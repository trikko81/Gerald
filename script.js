function updateWeather() {
    const apiKey = 'd601d7d03db040334f6f47792d15e86d';
    const city = 'New York';

    fetch(`https://api.openweathermap.org/data/2.5/weather?q=${city}&appid=${apiKey}&units=imperial`)
        .then(response => response.json())
        .then(data => {
            const day = new Date(data.dt * 1000);
            const date = `${day.getMonth() + 1}/${day.getDate()}/${day.getFullYear()}`;
            const time = day.toLocaleTimeString();

            document.getElementById('day').textContent = day.toLocaleString('en-US', { weekday: 'long' }); 
            document.getElementById('date').textContent = date;
            document.getElementById('time').textContent = time;
            document.getElementById('temperature').textContent = `${Math.round(data.main.temp)}°F`;
            document.getElementById('air-quality').textContent = `Pessure: ${data.main.pressure} hPa`;
            document.getElementById('wind-speed').textContent = `Wind: ${data.wind.speed} mph`;
            document.getElementById('feels-like').textContent = `Feels like: ${Math.round(data.main.feels_like)}°F`;
        })
        .catch(err => {
            console.log("Error weather data a bitch wahh wahh wahh", err);
        });
}
