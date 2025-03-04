# Auto.EDA
A tool for automating exploratory data analysis (EDA), offering quick insights and visualizations

## How it works

### Dataset Input
- User provides the dataset file path.
- The app loads the dataset into a Pandas DataFrame.

### Dataset Summary
- **Display:**
  - AI Summary of Dataset
  - Basic structure (shape, column names, data types).
  - Sample of the data.
  - Missing values (count for each column).
  - Descriptive statistics.

### AI-Powered Summary
- Collects `df.head()`.
- Passes these to the AI inference model (using LangChain with ChatGoogleGenerativeAI).
- The AI generates a human-readable summary, explaining what the dataset might represent and what it can be used for (e.g., "This dataset likely represents real estate listings for houses. The data could be used for predicting house prices").

### Graphs
- AI model decides:
  - Which columns/features are relevant for visualization.
  - The types of graphs to generate (e.g., bar chart, scatter plot, heatmap).
- Automatically creates and displays graphs using Matplotlib or Plotly.
- Graphs are generated based on AI recommendations.

## Installation

To install and run the application, follow these steps:

1. Clone the repository:
   ```sh
   git clone https://github.com/kabillanta/Auto.EDA.git
   ```
2. Navigate to the project directory:
   ```sh
   cd Auto.EDA
   ```
3. Install the necessary dependencies:
   ```sh
   pip install -r requirements.txt
   ```
4. Run the application:
   ```sh
   streamlit run main.py
   ```

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository.
2. Create a new branch:
   ```sh
   git checkout -b feature
   ```
3. Commit your changes:
   ```sh
   git commit -m "Add feature"
   ```
4. Push to the branch:
   ```sh
   git push origin feature
   ```
5. Open a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

