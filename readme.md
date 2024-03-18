## Project Name: Weather Data Processing with OpenWeather API and Database Insertion

### Overview:
This project utilizes the OpenWeather API to fetch weather data, saves the output in a JSON file, performs data transformations including fixing date formats, and inserts the processed data into a database.

### Setup Instructions:
1. Clone this Github repository.
2. Copy `.env-dist-prod` to `.env` in the root directory. 🔒
3. Update the Airflow password 🔑 in the `.env` file. 
4. Navigate to the `service` folder 📁 and ensure the API key is correctly set in the `.env` file.

### Docker Setup:
1. Ensure Docker is installed on your system.
2. Move to finix_airflow folder 📁
3. Run the following command to start the Docker container:
   ```shell
   sudo docker-compose -f docker-compose.yaml up --build -d 
   ```

### Airflow Configuration:
1. For more information on Airflow, visit the official [Airflow repository](https://github.com/apache/airflow).
2. Below is an image of Airflow for reference:

   Airflow Image

### Additional Notes:
- Remember to copy `.env-dist-prod` to `.env` before starting the Docker container. 🔒
- Make sure to update necessary configurations in both `.env` files.🔑
- For any issues or questions, please refer to the project's documentation or contact the project maintainers.

🌤️ Happy Weather Data Processing! 🌦️