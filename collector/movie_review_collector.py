import math
import re
import requests
from bs4 import BeautifulSoup
from db.MovieDAO import MovieDAO
from common.log_config import LogConfig


class MovieReviewCollector:
    def __init__(self, movie_code):
        self.movieDao = MovieDAO()
        self.logConfig = LogConfig()
        self.log = self.logConfig.get_logger()
        self.movie_code = movie_code

    def movie_title_crawler(self):
        url = 'https://movie.naver.com/movie/bi/mi/point.naver?code={}'.format(self.movie_code)
        
        # requests.get() 사용시 SSL Error 나면 → requests.get(url, verify=False) 옵션을 추가하면 HTTPS 요청에 대한 SSL 인증서 과정 생략 가능
        result = requests.get(url)
        soup = BeautifulSoup(result.text, 'html.parser')
        title = soup.select('h3.h_movie > a')[0].get_text()
        return title

    def movie_review_crawler(self):
        title = self.movie_title_crawler()

        self.log.info(f'>> Start collecting movies for "{title}"')
        url = 'https://movie.naver.com/movie/bi/mi/pointWriteFormList.naver?code={}&type=after&isActualPointWriteExecute=false&isMileageSubscriptionAlready=false&isMileageSubscriptionReject=false&page=1'.format(
            self.movie_code)
        result = requests.get(url)
        soup = BeautifulSoup(result.text, 'html.parser')
        all_count = soup.select('strong.total > em')[0].get_text()
        numbers = re.sub(r'[^0-9]', '', all_count)  # 정규식 활용 => 0~9숫자 외의 값은 ''으로 제거
        pages = math.ceil(int(numbers) / 10)
        self.log.info(f'>> The total number of pages to collect is {pages}')

        count = 0

        for page in range(1, pages + 1):
            url = 'https://movie.naver.com/movie/bi/mi/pointWriteFormList.naver?code={}&type=after&isActualPointWriteExecute=false&isMileageSubscriptionAlready=false&isMileageSubscriptionReject=false&page={}'.format(
                self.movie_code, page)

            result = requests.get(url)
            doc = BeautifulSoup(result.text, 'html.parser')
            all_count = doc.select('score_total > string.total > em')

            review_list = doc.select('div.score_result > ul > li')
            for i, one in enumerate(review_list):
                count += 1
                print('========================================================================')
                print(f'== Review {count} ===================================================')

                # review 정보 수집
                review = one.select('div.score_reple > p > span')[-1].get_text().strip()

                # review 정보 수집
                score = one.select('div.star_score > em')[0].get_text()

                # 작성자(닉네임) 정보 수집
                original_writer = one.select('div.score_reple dt > em')[0].get_text().strip()
                idx_end = original_writer.find('(')
                writer = original_writer[:idx_end]

                # Date 정보 수집
                original_date = one.select('div.score_reple dt > em')[1].get_text()
                date = original_date[:10]
                print('# Review: {}'.format(review))
                print('# Score: {}'.format(score))
                print('# Writer: {}'.format(writer))
                print('# Date: {}'.format(date))

                # 수집한 리뷰 데이터 저장
                # 1) dict type 생성
                data = {'title': title,
                        'score': score,
                        'review': review,
                        'writer': writer,
                        'date': date}
                # 2) data 저장
                self.movieDao.add_review(data)
            page += 1
        self.log.info(f'>> {count} reviews completed')
