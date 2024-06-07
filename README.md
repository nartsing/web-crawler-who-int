# web-crawler-who-int
## Project Overview
Web-Crawler-WHO-Int is a web scraping tool designed to extract data from the World Health Organization (WHO) Mortality Database. Specifically, it targets the "Injuries" theme available at [this link](https://platform.who.int/mortality/themes/theme-details/mdb/injuries). This tool is useful for researchers, data analysts, and public health professionals who need to gather and analyze mortality data related to injuries.

## Usage
To run the web crawler, execute the main script with the necessary parameters. The crawler will fetch and parse the data from the specified WHO Mortality Database page.

```shell
python3 run.py
```

**Note**: You need to configure the spider_cfg.json file with the paths to Chrome and Chromedriver.


## Data Convert
This code includes a set of data obtained through web scraping, located in the `data_convert/` directory. The raw data is contained in data.zip. After unzipping it using `unzip data.zip`, you can convert it to `data.csv` using the script `data_convert/convert2csv.py`.