# Brighter Potential
<div id="top"></div>
<!--
*** Thanks for checking out the Best-README-Template. If you have a suggestion
*** that would make this better, please fork the repo and create a pull request
*** or simply open an issue with the tag "enhancement".
*** Don't forget to give the project a star!
*** Thanks again! Now go create something AMAZING! :D
-->



<!-- PROJECT SHIELDS -->
<!--
*** I'm using markdown "reference style" links for readability.
*** Reference links are enclosed in brackets [ ] instead of parentheses ( ).
*** See the bottom of this document for the declaration of the reference variables
*** for contributors-url, forks-url, etc. This is an optional, concise syntax you may use.
*** https://www.markdownguide.org/basic-syntax/#reference-style-links
--



<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/annieco29/rooftop_solar_energy_app">
    <img src="apps/brighter_potential_logo.png" alt="Logo" width="80" height="80">
  </a>

  <h3 align="center">Brighter Potential: Predicting Rooftop Solar Energy Potential</h3>

  <p align="center">
    Brighter Potential is a machine learning app that I created for the University of Florida and IBM Hackathon in Fall 2021. It allows Florida energy market stakeholders to predict and measure the solar rooftop potential in the most populated areas of Florida. Brighter Potential taps into Florida’s prospective residential and industrial solar rooftop production to display how a renewable source such as solar can meet the energy demands of Florida.
    <br />
    <a href="https://github.com/annieco29/rooftop_solar_energy_app"><strong>Explore the docs »</strong></a>
    <br />
    <br />
<a href="http://169.51.195.94:32588/">View Demo</a>

  </p>
</div>



<!-- TABLE OF CONTENTS -->
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
      <a href="#getting-started">How to View Dashboard</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

MAPPING PRODUCTION POTENTIAL VS. DEMAND

* On the first tab, The choropleth map displays a prediction of the percentage of energy demand that could be supplied by solar energy if the total rooftop solar capacity were utilized 
* This prediction is created using an xgboost and a regression model that predict daily energy demand and daily rooftop solar energy, respectively, using weather data from 2019 as inputs. (we used available weather data from 2019, but predictions could be made in real time based on data availability) 
* The daily rooftop solar energy prediction additionally uses building rooftop capacity data by zipcode to project the approximate number of solar panels that could be added by zip code. 
* Here on the map we have aggregated the daily predictions to monthly capacity, with a month selector along the side.
* This prediction could be used for stakeholders to maximize their marketing to consumers in certain regions.

<a href="https://github.com/annieco29/rooftop_solar_energy_app">
    <img src="front_end/measuring_production.png" alt="pic1" width="300" height="300">
  </a>


LEVERAGING INDUSTRIAL BUILDINGS
* Industrial buildings such as factories have some of the greatest rooftop solar potential due to the large surface area they provide for solar panels. 
* Industrial sites could significantly help support Florida’s energy grid. 
* By clicking the “View Industrial Locations,” checkbox the map will display the locations for industrial real estate sites larger than 750,000 sqft. 
* By clicking on a given industrial site point in the app, a stakeholder can view the owner of the property, as well as the average daily solar production capacity as predicted by the regression model. 
* This allows stakeholders to target industrial real estate sites for additional rooftop solar power capacity. 

IDENTIFYING TIME PERIODS FOR SAVINGS POTENTIAL
* The Solar Savings Potential tab allows a policy maker or stakeholder to view the solar capacity as compared to predicted energy demand by zip code and by custom time periods from 2019 by changing the fields in the side bar. 
* The hierarchical sunburst chart allows stakeholders to view the different months of the year that have low amounts of solar production coverage so that they can plan for time periods where supplemental power sources are needed. 
* Blue indicates high predicted solar energy coverage, and pink/red indicates low predicted solar energy coverage. 
METHODOLOGY AND MODEL PERFORMANCE

* The “Predictive Model Methodology” tab shows the predictive power of the xgboost model that predicts daily energy demand and the linear regression model that predicts solar energy production. 
* The plots show how well the models performed on our test data sets, which are from from two different data sets listed in a future slide. 
* We see that the machine learning models on the backend of the Brighter Potential application predict energy demand and solar production with low error.

<p align="right">(<a href="#top">back to top</a>)</p>



### Built With

These are the major frameworks/libraries used for this project.

* [python](https://python.org/)
* [Streamlit](https://streamlit.io/)
* [plotly](https://plotly.com/)

Deployed on:

* [IBM Cloud using Kubernetes](https://ibm.com/)

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- How to see it -->
## How to view the Brighter Potential dashboard

The 

### Prerequisites

This is a list of libraries you need to spin up the Streamlit dashboard and how to install them.
* streamlit
  ```sh
  pip install streamlit
  ```
 * multiapp
  ```sh
  pip install multiapp
  ```
 * pandas
  ```sh
  pip install pandas
  ```
 * plotly
  ```sh
  pip install ploty
  ```

<!-- ### Installation

_Below is an example of how you can instruct your audience on installing and setting up your app. This template doesn't rely on any external dependencies or services._

1. Clone the repo
   ```sh
   git clone https://github.com/annieco29/rooftop_solar_energy_app.git
   ```
2. From your commmand line, run the following:
   ```she
   streamlit run app.py
   ```

<p align="right">(<a href="#top">back to top</a>)</p>
 -->


<!-- USAGE EXAMPLES -->
## Usage

Use this space to show useful examples of how a project can be used. Additional screenshots, code examples and demos work well in this space. You may also link to more resources.

_For more examples, please refer to the [Documentation](https://example.com)_

<p align="right">(<a href="#top">back to top</a>)</p>

<!-- LICENSE -->
## License

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- CONTACT -->
## Contact
 

Project Link: [https://github.com/annieco29/rooftop_solar_energy_app](https://github.com/annieco29/rooftop_solar_energy_app)

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- ACKNOWLEDGMENTS -->
## Acknowledgments

TBC

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/othneildrew/Best-README-Template.svg?style=for-the-badge
[contributors-url]: https://github.com/othneildrew/Best-README-Template/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/othneildrew/Best-README-Template.svg?style=for-the-badge
[forks-url]: https://github.com/othneildrew/Best-README-Template/network/members
[stars-shield]: https://img.shields.io/github/stars/othneildrew/Best-README-Template.svg?style=for-the-badge
[stars-url]: https://github.com/othneildrew/Best-README-Template/stargazers
[issues-shield]: https://img.shields.io/github/issues/othneildrew/Best-README-Template.svg?style=for-the-badge
[issues-url]: https://github.com/othneildrew/Best-README-Template/issues
[license-shield]: https://img.shields.io/github/license/othneildrew/Best-README-Template.svg?style=for-the-badge
[license-url]: https://github.com/othneildrew/Best-README-Template/blob/master/LICENSE.txt
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/in/othneildrew
[product-screenshot]: images/screenshot.png
