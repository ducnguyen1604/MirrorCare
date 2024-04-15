import React, { useEffect, useRef, useState } from 'react';
import './App.css';

const API_KEY = 'a634638c76784cd4ff382858dd608d7f';

function App() {
  const videoRef = useRef(null);
  const [currentTime, setCurrentTime] = useState('');
  const [currentSecond, setCurrentSecond] = useState('');
  const [currentDate, setCurrentDate] = useState('');
  const [weatherData, setWeatherData] = useState({ temperature: '', humidity: '' });
  const [medicineCount, setMedicineCount] = useState(1); // Default medicine count
  const [messageOfTheDay, setMessageOfTheDay] = useState('');
  const [messagePool, setMessagePool] = useState([]);
  const [reminderData, setReminderData] = useState({ data1: '', data2: '' });
  const [dayImage, setDayImage] = useState('morning.png'); // Default image
  
  useEffect(() => {
//---------------------------------------------------------
    // Set up interval to update live time and date every second
    const TimeIntervalId = setInterval(() => {
      const now = new Date();
      const formattedTime = now.toLocaleTimeString('en-US', { hour: 'numeric', minute: '2-digit', hour12: true });
      const formattedSecond = now.toLocaleTimeString('en-US', { second: '2-digit', hour12: true });
      const monthAbbreviation = now.toLocaleString('default', { month: 'short' }).toUpperCase();
      const dayOfMonth = now.getDate();
      const dayOfWeek = now.toLocaleDateString('en-US', { weekday: 'short' }).toUpperCase();
      setCurrentTime(`${formattedTime}`);
      setCurrentSecond(`${formattedSecond}`);
      setCurrentDate(`${monthAbbreviation} ${dayOfMonth}, ${dayOfWeek}`);
      fetchReminders();
    }, 1000);

    // Fetch weather data for Singapore every 5 minutes
    const weatherIntervalId = setInterval(() => {
      fetchWeatherData();
    }, 300000);

//---------------------------------------------------------
    // Call updateDayImage after setting up intervals
    updateDayImage(new Date());

    // Start webcam when the component mounts
    startWebcam();

    // Call the function to update the message
    updateMessageOfTheDay();

    // Call the function to fetch messages
    fetchMessages();

    // Initial fetch of weather data
    fetchWeatherData();

    // Call the function to fetch reminders
    fetchReminders();
//---------------------------------------------------------
    // Cleanup: Stop the webcam and clear the intervals when the component unmounts
    return () => {
      const tracks = videoRef.current?.srcObject?.getTracks();
      tracks?.forEach((track) => track.stop());
      clearInterval(TimeIntervalId);
      clearInterval(weatherIntervalId);
    };
  }, []);
//---------------------------------------------------------

  const startWebcam = async () => {
    try {
      // Get user media
      const stream = await navigator.mediaDevices.getUserMedia({ video: true });

      // Set the video source to the webcam stream
      if (videoRef.current) {
        videoRef.current.srcObject = stream;
      }
    } catch (error) {
      console.error('Error accessing webcam:', error);
    }
  };


  const updateDayImage = (time) => {
    const hour = time.getHours();
    let newDayImage = 'morning.png';

    if (hour >= 5 && hour < 12) {
      newDayImage = 'morning.png';
    } else if (hour >= 12 && hour < 17) {
      newDayImage = 'afternoon.png';
    } else if (hour >= 17 && hour < 20) {
      newDayImage = 'evening.png';
    } else {
      newDayImage = 'night.png';
    }

    // Update the day image only if it has changed
    if (newDayImage !== dayImage) {
      setDayImage(newDayImage);
    }
  };
  


  const fetchMessages = async () => {
    try {
      const response = await fetch('/images/MOTD.txt');  // Adjust the path accordingly
      const text = await response.text();
      const messages = text.split('\n').filter((message) => message.trim() !== '');

      setMessagePool(messages);
    } catch (error) {
      console.error('Error fetching messages:', error);
    }
  };


  const updateMessageOfTheDay = () => {
    const now = new Date();
    const currentDay = now.getDate();

    // Check if it's a new day
    if (currentDay !== localStorage.getItem('currentDay')) {
      // Select a random message from the pool
      const randomIndex = Math.floor(Math.random() * messagePool.length);
      const newMessage = messagePool[randomIndex];

      // Update the state and store the current day in local storage
      setMessageOfTheDay(newMessage);
      localStorage.setItem('currentDay', currentDay);
    }
  };


  const fetchWeatherData = async () => {
    try {
      const response = await fetch(`https://api.openweathermap.org/data/2.5/weather?q=Singapore&appid=${API_KEY}`);
      const data = await response.json();
      const temperature = (data.main.temp - 273.15).toFixed(2); // Convert Kelvin to Celsius
      const humidity = data.main.humidity;
      setWeatherData({ temperature, humidity });
    } catch (error) {
      console.error('Error fetching weather data:', error);
    }
  };

  const fetchReminders = async () => {
    try {
      const response = await fetch('/images/reminder.txt'); // Adjust the path accordingly
      const text = await response.text();
      const reminderLines = text.split('\n').filter((line) => line.trim() !== '');
  
      // Extract data for Reminder 1 and Reminder 2
      const [data1, data2] = reminderLines.map((line) => {
        const [, data] = line.split(':');
        return data.trim();
      });
  
      // Update state with the fetched data
      setReminderData({ data1, data2 });
    } catch (error) {
      console.error('Error fetching reminders:', error);
    }
  };

  return (
    <>
      <div style={{ textAlign: 'center', marginBottom: '10px', marginTop: '-20px', border: '4px solid lightgreen', borderRadius: '10px', padding: '10px', backgroundColor: 'black' }}>
        <div style={{ fontSize: '35px', fontWeight: 'bold', margin: '0px 10px 0px 0', color: 'yellow', display: 'inline-block' }}>
          <img src={`/images/${dayImage}`} alt="Clock Icon" style={{ width: '40px', height: '40px', marginRight: '10px' }} />
          {currentTime}
        </div>
        <div style={{ fontSize: '35px', fontWeight: 'bold', margin: '0', color: 'white', display: 'inline-block', marginLeft: '10px' }}>{currentDate}</div>

        <div style={{ display: 'flex', justifyContent: 'center' }}>
          <img src="/images/temp.png" alt="Temperature Icon" style={{ width: '40px', height: '40px', marginRight: '10px' }} />
          <p style={{ fontSize: '35px', fontWeight: 'bold', margin: '-2px 10px 5px 0', color: `rgb(255, 105, 180)` }}>
            {weatherData.temperature}°C
          </p>

          <img src="/images/humid.png" alt="Humidity Icon" style={{ width: '40px', height: '40px', marginRight: '10px' }} />
          <p style={{ fontSize: '35px', fontWeight: 'bold', margin: '-2px 10px 5px 0', color: `rgb(0, 191, 255)` }}>
            {weatherData.humidity}%
          </p>

          <img src="/images/med.png" alt="Medicine Icon" style={{ width: '40px', height: '40px', marginRight: '10px' }} />
          <p style={{ fontSize: '35px', fontWeight: 'bold', margin: '-2px 10px 5px 0', color: `rgb(255, 105, 180)` }}>
            {medicineCount}
          </p>

        </div>
        <p style={{ fontSize: '10px', color: 'white', margin: '-2px 0px -5px 0', whiteSpace: 'pre-line' }}>
          {messageOfTheDay}
        </p>
      </div>

      <div style={{ display: 'flex', alignItems: 'center', height: '87vh' /* Adjust the height as needed */ }}>
        <video ref={videoRef} autoPlay playsInline style={{ maxWidth: '100%', maxHeight: '100%', width: '100%', height: '100%', borderRadius: '10px', border: '4px solid lightgreen', objectFit: 'cover'}} />
      </div>

      <div style={{ textAlign: 'center', marginTop: '20px', borderRadius: '10px', maxWidth: '100%' }}>
        <table style={{ borderCollapse: 'collapse', width: '100%', margin: 'auto', marginTop: '-10px', backgroundColor: 'black', borderRadius: '10px' }}>
          <thead>
            <tr>
              <th style={{ color: 'white' }}>Reminder 1:</th>
              <th style={{ color: 'white' }}>{reminderData.data1}</th>
              {/* Add more columns as needed */}
            </tr>
          </thead>
          <tbody>
            <tr>
              <th style={{ color: 'white' }}>Reminder 2:</th>
              <th style={{ color: 'white' }}>{reminderData.data2}</th>
              {/* Add more data rows as needed */}
            </tr>
          </tbody>
        </table>
      </div>
    </>
  );
}

export default App;