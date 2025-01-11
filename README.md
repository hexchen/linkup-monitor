
# Freestyle Libre 3 Glucose Reader

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Contributions Welcome](https://img.shields.io/badge/contributions-welcome-brightgreen.svg)

A console-based application to fetch glucose measurements from your Freestyle Libre 3 sensor and provide real-time metrics for monitoring and visualization. The application is designed for tech-savvy diabetics and caregivers who want to seamlessly integrate glucose tracking into their existing monitoring stacks using Prometheus and Grafana.

**Disclaimer:** This project is not affiliated with or endorsed by Abbott Laboratories, the manufacturer of the Freestyle Libre 3 sensor. Freestyle Libre is a trademark of Abbott Laboratories.

---

## Features

- **Real-time Glucose Measurements**: Fetch and display your glucose readings directly in the console.
- **Prometheus Metrics Export**: Expose glucose metrics in a Prometheus-compatible format for easy scraping.

---

## Getting Started

### Prerequisites

- A Freestyle Libre 3 sensor
- An account on https://www.librelinkup.com/ hooked up with your freestyle libre account
- Prometheus (optional, for metrics scraping)
- Grafana (optional, for visualization)

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/mstiehr-dev/linkup-monitor.git
   cd linkup-monitor
   ```

2. Install the required Python packages:
   ```bash
   pip install -r requirements.txt
   ```

3. Configure the application:
   Copy `linkup_config.json.skel` to `linkup_config.json` and enter the credentials to your librelinkup account.

### Running the Application

To start the console application:
```bash
python main.py
```

Or use the prebuilt container image:
```bash
podman run --rm -d -p 8000:8000 --name linkup -v $(pwd)/linkup_config.json:/app/linkup_config.json -w /app martinstiehr/libre-monitor:latest
```

---

## Integration with Prometheus and Grafana

1. **Prometheus**:
   - Add the following scrape configuration to your `prometheus.yml`:
     ```yaml
     scrape_configs:
       - job_name: 'glucose_reader'
         static_configs:
           - targets: ['localhost:8000']
     ```
   - Replace `localhost:8000` with your application's metrics endpoint.

2. **Grafana**:
   - Add Prometheus as a data source in Grafana.
   - Visualize your glucose trends using metrics such as `glucose_level` and `timestamp`.

---

## Example Output

### Console
```
2025-01-09 16:02:19 - INFO - Value: 13.8 mmol/L (1/09/2025 4:01:47 PM)
```

### Prometheus Metrics
```
# HELP glucose_measurement glucose measurement in mmol/L
# TYPE glucose_measurement gauge
glucose_measurement 13.8

# HELP glucose_measurement_out_of_boundaries glucose measurement is high or low
# TYPE glucose_measurement_out_of_boundaries gauge
glucose_measurement_out_of_boundaries 0.0

```

---

## Contributing

Contributions are welcome! If you have ideas, feature requests, or bug reports, please open an issue or submit a pull request.

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## Acknowledgments

- [Prometheus](https://prometheus.io/)
- [Grafana](https://grafana.com/)
- [LibreLinkUp](https://www.librelinkup.com)
- The open-source community for their amazing tools and libraries.

---

Happy monitoring and stay healthy! If you enjoy this project, consider giving it a ⭐ on [GitHub](https://github.com/mstiehr-dev/linkup-monitor).

