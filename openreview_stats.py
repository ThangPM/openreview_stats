from requests_html import HTMLSession
from bs4 import BeautifulSoup
from tqdm import tqdm

import pandas as pd
import statistics


if __name__ == '__main__':

    openreview_url = "https://openreview.net"
    confs = {"neurips2021": 5, "neurips2022": 8}
    column_names = ["Paper_title", "URL", "Review_scores", "Average"]

    session = HTMLSession()

    for conf, no_pages in confs.items():
        print("Extracting review scores for conference {}...".format(conf))

        results = []
        for i in range(0, no_pages):
            print("Extracting at page {}...".format(i+1))

            html = ""
            with open("data/{}/page{}.txt".format(conf, i+1), "r") as input_file:
                for line in input_file:
                    html += line

            soup = BeautifulSoup(html, features='lxml')
            submissions = [(a.text.replace("\n", "").strip(), a.attrs['href']) for a in soup.find_all('a', href=True) if a.attrs['href'].startswith("/forum?id=")]
            page_results = []

            for submission in tqdm(submissions):
                sub_url = openreview_url + submission[1]
                r = session.get(sub_url)
                r.html.render(sleep=2)

                soup = BeautifulSoup(r.html.html, features='lxml')
                all_scores = [span.text for span in soup.find_all("span", {"class": "note_content_value"}) if any([span.text.startswith(x) for x in ["1:", "2:", "3:", "4:", "5:", "6:", "7:", "8:", "9:", "10:"]])]
                review_scores = [int(score.split(":")[0]) for idx, score in enumerate(all_scores) if idx % 2 == 0]
                confidence_scores = [int(score.split(":")[0]) for idx, score in enumerate(all_scores) if idx % 2 == 1]

                results.append([submission[0], openreview_url + submission[1], review_scores, statistics.mean(review_scores) if len(review_scores) > 0 else 0])
                page_results.append(results[-1])

            [print("Title:\t{0}\tURL:\t{1}\tReview_scores\t{2}\tAverage:\t{3}".format(*result)) for result in page_results]

        df = pd.DataFrame(results, columns=column_names)
        df.sort_values(by=["Average"])
        df["Rank"] = list(range(1, len(df) + 1))
        df.to_csv("results/{}.csv".format(conf))

    print("Finish!")


