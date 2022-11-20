
## ARTICLES API

<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
  </ol>
</details>


### About The Project
  Data collection of NBS articles.
<p align="right"><a href="#top">back to top</a></p>

#### Build With
* [Scrapy Framework](https://scrapy.org/)
* [JSON Schema](https://json-schema.org/)
* [sqlite3](https://www.sqlite.org/index.html)
* [sqlachemy](https://www.sqlalchemy.org/)
* [Selenium WebDriver](https://www.selenium.dev/documentation/webdriver/)
* [Fast API](https://fastapi.tiangolo.com/)

### Getting Started
#### Installation
1. Clone the repo
   ```sh
   git clone https://github.com/TanyaAng/Automated_Shear_Walls_Calculations.git
   ```
2. Install all Python libraries
   ```sh
   pip install -r requirements.txt
   ```
3. Make nbs_articles Root directory

<p align="right"><a href="#top">back to top</a></p>

### Usage


<p align="right"><a href="#top">back to top</a></p>

### Roadmap

| Datapoint                | HTTP Method | Description                                   |
| ------------------------ | ----------- | --------------------------------------------- |
| /articles/               | GET         | get all crawled articles and their propertirs |
| /articles/?label={label} | GET         | get list of articles with the same label      |
| /articles/?date={date}   | GET         | get list of articles from the date            |
| /article/{article_id}    | GET         | get single article                            |
| /article/{article_id}    | DELETE      | delete singel article                         |
| /article/{article_id}    | PUT         | update singel article                         |


<p align="right"><a href="#top">back to top</a></p>

### License
MIT License

<p align="right"><a href="#top">back to top</a></p>

### Contact

Tanya Angelova - [LinkedIn](https://www.linkedin.com/in/tanya-angelova-44b03590/) - t.j.angelova@gmail.com

Project Link: [github link]

<p align="right"><a href="#top">back to top</a></p>

[LinkedIn]: https://www.linkedin.com/in/tanya-angelova-44b03590/
[github link]: https://github.com/TanyaAng/Automated_Shear_Walls_Calculations
