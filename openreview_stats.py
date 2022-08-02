from requests_html import HTMLSession
from bs4 import BeautifulSoup
import statistics
from tqdm import tqdm


if __name__ == '__main__':
    openreview_url = "https://openreview.net"
    confs = {"neurips2021": 5, "neurips2022": 8}

    session = HTMLSession()

    for conf, no_pages in confs.items():
        print("Extracting review scores for conference {}...".format(conf))

        for i in range(0, no_pages):
            print("Extracting at page {}...".format(i+1))
            results = {}
            html = ""

            with open("{}/page{}.txt".format(conf, i+1), "r") as input_file:
                for line in input_file:
                    html += line

            soup = BeautifulSoup(html, features='lxml')
            submissions = [(a.text.replace("\n", "").strip(), a.attrs['href']) for a in soup.find_all('a', href=True) if a.attrs['href'].startswith("/forum?id=")]

            for submission in tqdm(submissions):
                sub_url = openreview_url + submission[1]
                r = session.get(sub_url)
                r.html.render(sleep=2)

                soup = BeautifulSoup(r.html.html, features='lxml')
                all_scores = [span.text for span in soup.find_all("span", {"class": "note_content_value"}) if any([span.text.startswith(x) for x in ["1:", "2:", "3:", "4:", "5:", "6:", "7:", "8:", "9:", "10:"]])]
                review_scores = [int(score.split(":")[0]) for idx, score in enumerate(all_scores) if idx % 2 == 0]
                confidence_scores = [int(score.split(":")[0]) for idx, score in enumerate(all_scores) if idx % 2 == 1]

                results[openreview_url + submission[1]] = "Title:\t{}\tURL:\t{}\tReview_scores\t{}\tAverage:\t{}".format(submission[0], openreview_url + submission[1], review_scores, statistics.mean(review_scores) if len(review_scores) > 0 else 0)

            for key, value in results.items():
                print(value)

    print("Finish!")


