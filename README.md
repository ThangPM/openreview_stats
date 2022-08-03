# Openreview Stats

This is a fun project that helps researchers who submitted papers to any conferences from Openreview to easily retrieve and compare their review scores with others.
You may have better strategies for your rebuttal period if you know the current rank among the submissions.
We can also gain more insights from the rebuttal and see if it actually helps increase your change of acceptance by comparing review scores before and after the rebuttal (Note: Data will be updated after the rebuttal).

**TLDR**: *We collected [review scores](https://docs.google.com/spreadsheets/d/1OhSK5jimCyPNtpOmO05vB547X6LhVmsklKgi3p_4WUc/edit?usp=sharing) of the Dataset and Benchmark track for NeurIPS which has just been organized since 2021.*

If you are interested or have some ideas to improve this project, please see the [open issues](https://github.com/ThangPM/openreview_stats/issues) for a full list of proposed features (and known issues) or feel free to reach out to me (Thang Pham) at [thangpham@auburn.edu](thangpham@auburn.edu).

### Prerequisites

* Anaconda 4.10 or higher
* Python 3.9 or higher
* pip version 21 or higher

### Installation

1. Clone this repository

   ```sh
   git clone git@github.com:ThangPM/openreview_stats.git && cd openreview_stats
   ```

2. Create and activate a Conda environment

   ```sh
   conda create -n openreview_stats python=3.9
   conda activate openreview_stats
   ```

3. Install required libraries

   ```sh
   pip install -r requirements.txt
   ```
4. Run the code to retrieve review scores for accepted papers (NeurIPS-2021) and under-reviewed papers (NeurIPS-2022).

    ```python
    python3 openreview_stats.py
    ```

### Collecting Results

Results are stored under `results` folder.
* results/neurips2021.csv
* results/neurips2022.csv
