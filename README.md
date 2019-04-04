# Analyzing nextbike in Berlin

<img src="https://biking.city/wp-content/uploads/2018/08/deezer-nextbike-bike-sharing-logo.jpg" width="150">

This was my final project in the data science bootcamp at Spiced Academy Berlin (Jan-Mar). The challenge was that there is no trip data like for the famous Chicago Bike sharing service Divvy https://www.divvybikes.com/system-data. I had to pull regular snapshots (1 every minute) of the stations and the available bikes. Whenever a bike left one station and shortly after appeared in another station, I generated that trip. There is a lot of data wrangling and the fun part was to analyze and visualize on folium maps.



## Why bike sharing?

I recently gave up my car and love the mobility offerings in Berlin. Moreover, I have a passion for mobility topics. Bike sharing has many economical, environmental and social advantages:
- Increased Connectivity
- Health & Exercise Benefits
- Bike sharing Makes Areas More Vibrant and Livable
- Offers More Equitable Transportation to Lower Income Areas
- Minimal Carbon Emission
- Lowest cost-per-mile public transport option
- It’s fun :-)


### Prerequisites

These are the main packages that I have used:

```
requests==2.21.0
beautifulsoup4==4.7.1
fbprophet==0.4.post2
folium==0.8.3
imageio==2.5.0
matplotlib==3.0.3
numpy==1.16.2
pandas==0.24.2
scipy==1.2.1
seaborn==0.9.0
selenium==3.141.0
```

### Analysis

Analyzed data for Berlin: 
* 17 days
* 243 stations
* 2778 bikes
* 9728 trips (raw file of trips: https://github.com/steffmul/nextbike/blob/master/all_trips.csv)

Trips per hour (gif shows only few days)

![Sample of few hours](https://raw.githubusercontent.com/steffmul/nextbike/master/nextbike_sample.gif)

Nextbike offers stations and allows for bikes to be parked inside the flex zone (floating). The starting point of trips stations vs floating bikes. The denser map shows the floating bikes.

![Heatmap of stations vs floating](https://raw.githubusercontent.com/steffmul/nextbike/master/floating%20vs%20stations2.gif)

Using FB Prophet to forecast daily or hourly demand

![Forecasting daily or hourly demand](https://raw.githubusercontent.com/steffmul/nextbike/master/forecast.gif)



## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* Hat tip to anyone whose code was used
* my great teachers at Spiced Academy: 
```
Kristian Rother https://github.com/krother
Paul Pawlodkowski https://github.com/pawlodkowski
Tom Gadsby
```
* Great thanks for Constantin, who made such an effort to document different APIs https://github.com/ubahnverleih
