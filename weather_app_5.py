# making this an object oriented is the aim of this version
import streamlit as st
import requests
from matplotlib import dates
from matplotlib import pyplot as plt
import numpy as np
API_KEY = "c7e5f321aee52de30dcc497147c25a6a"

class Conversion:
    def __init__(self,unit, temp_kelvin):
        self.temp_kelvin=temp_kelvin
        self.unit=unit

    def conversion(self):
        if self.unit=="Kelvin":
            return self.in_kelvin()
        elif self.unit=="Celsius":
            return self.to_celsius()
        elif self.unit=="Fahrenheit":
            return self.to_fahrenheit()

    def in_kelvin(self):
        return round(self.temp_kelvin)
    #function to convert kelvin to celsius
    def to_celsius(self):
        return round(self.temp_kelvin - 273.15)
    #function to convert kelvin to fahrenheit
    def to_fahrenheit(self):
        return round(9 / 5 *(self.temp_kelvin - 273.15) + 32)

class Weather:
    def __init__(self, city,unit):
        self.city=city
        self.unit=unit

    #function to find current weather
    def find_current_weather(self):
        base_url =f"https://api.openweathermap.org/data/2.5/weather?q={self.city}&appid={API_KEY}"
        weather_data = requests.get(base_url).json()
        try:
            general = weather_data['weather'][0]['main']
            icon_id = weather_data['weather'][0]['icon']
            lat = weather_data['coord']['lat']
            lon = weather_data['coord']['lon']
            humidity = weather_data['main']['humidity']
            wind_speed = weather_data['wind']['speed']
            temp=Conversion(self.unit,weather_data['main']['temp'])
            temperature=temp.conversion()
            icon = f"https://openweathermap.org/img/wn/{icon_id}@2x.png"
        except KeyError:
            st.error("City Not Found")
            st.stop()
        return general, temperature, icon, lat, lon, humidity, wind_speed

#function to get five day forcast datas
class ForcastData:
    def __init__(self,lat,lon):
        self.lat=lat
        self.lon=lon
        self.url_2=f"https://api.openweathermap.org/data/2.5/forecast?lat={self.lat}&lon={self.lon}&appid={API_KEY}"
        self.forcast=requests.get(self.url_2).json()

    def max(self,day):
        i=day*8
        return self.forcast['list'][i]['main']['temp_max']
    
    def min(self,day):
        i=day*8
        return self.forcast['list'][i]['main']['temp_min'] 
    
    def date(self,day):
        i=day*8
        return self.forcast['list'][i]['dt_txt']
        
    def five_day_forcast(self):
        temp=ForcastData(self.lat, self.lon)
        max_y=[temp.max(i) for i in range(0,5,1)]
        min_y=[temp.min(i) for i in range(0,5,1)]
        date=[temp.date(i) for i in range(0,5,1)]
        
        return max_y,min_y, date
            
# main function frontent features are written in main function
def main():
    st.title("Find the weather") 
    subtitle = st.write("### Write the name of a City and select the Temperature Unit and Graph Type from the Sidebar")
    city =st.text_input("Enter the Name of a City").lower()
    unit= st.selectbox("Select Temperature Unit",("Celsius", "Fahrenheit","Kelvin"))
    g_type=st.selectbox("Select Graph Type",("Line Graph","Bar Graph"))
    if st.button("Find"):
        if city=="":
            pass
        else:
            while city[-1]==" "and city!=" ":
                city=city[0:-1]
            while city[0]==" " and city!=" ":
                city=city[1:]
        weather=Weather(city, unit)
        general, temperature, icon, lat, lon, humidity, wind_speed = weather.find_current_weather()
        st.write("## Live Weather Conditions")
        col_1, col_2, col_3, col_4= st.columns(4)
        with col_1:
            if unit=="Celsius":
                st.metric(label="Temperature", value=f"{temperature}°C")
            if unit == "Kelvin":
                st.metric(label="Temperature", value=f"{temperature}K")
            if unit == "Fahrenheit":
                st.metric(label="Temperature", value=f"{temperature}°F")
        with col_2:
            st.metric(label="Humidity", value=f"{humidity}%")
        with col_3:
            st.metric(label="Wind Speed", value=f"{wind_speed}mph")
        with col_4:
            st.write(general)
            st.image(icon)
        st.write("## Weather Forcast")
        five_day_forcast=ForcastData(lat,lon)
        max_y, min_y, date= five_day_forcast.five_day_forcast()
        days= ["Day 1", "Day 2", "Day3","Day 4", "Day 5"]
        
        # Create two line plots
        if g_type=="Bar Graph":
            x=np.arange(len(days))
            fig, ax = plt.subplots()
            w=0.35
            min_x=[i+w for i in x]
            cel_min_y=[float(j-273.15) for j in min_y]
            cel_max_y=[float(k-273.15) for k in max_y]
            ax.bar(x, cel_max_y,width=w,label='Maximum Temperature')
            ax.bar(min_x, cel_min_y,width=w,label='Minimum Temperature')
            plt.xticks(min_x , days)
            ax.set_xlabel('Days')                       
            ax.set_ylabel('Temperature (°C)')                
            ax.set_title('5 Day Weather Forcast')       
            ax.legend()                                 
            st.pyplot(fig)
        else:
            x=np.arange(len(days))
            fig, ax = plt.subplots()
            w=0.35
            min_x=[i+w for i in x]
            cel_min_y=[float(j-273.15) for j in min_y]
            cel_max_y=[float(k-273.15) for k in max_y]
            ax.plot(x, cel_max_y,label='Maximum Temperature')
            ax.plot(min_x, cel_min_y,label='Minimum Temperature')
            plt.xticks(min_x , days) 
            ax.set_xlabel('Days')
            ax.set_ylabel('Temperature (°C)')
            ax.set_title('5 Day Weather Forcast')
            ax.legend() 
            st.pyplot(fig)

if __name__ == '__main__':
    main()