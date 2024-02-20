# Stock Overview Virtual Machine

This repository hosts the setup for a virtual machine (VM) dedicated to providing weekly stock overviews. The primary objectives are:

1. **Email Delivery**: Send an email every Friday at 12:00 PM containing an overview of randomly chosen stocks along with their performance.
2. **Data Retrieval**: Utilize the Yahoo Finance API to gather stock data.
3. **Visualization**: Create weekly performance visualizations for the selected stocks.

## Functionality

### Email Delivery

The VM is configured to send an email every Friday at noon containing a curated selection of stock information. This email includes a friendly message along with details on the performance of the chosen stocks.

### Data Retrieval

The Yahoo Finance API is integrated into the VM to fetch real-time stock data. This data is used to generate the stock overview for the email.

### Visualization

Additionally, the VM is designed to generate visualizations depicting the weekly performance of the selected stocks. These visualizations provide users with a graphical representation of how the stocks have fared over time.

## Usage

To utilize this VM:

1. Ensure you have the necessary dependencies installed, including Python and the required libraries.
2. Set up the VM according to the provided instructions.
3. Configure the email settings to match your preferences, including the recipient's email address and any custom message.
4. Schedule the VM to run every Friday at 12:00 PM.

## Contributions

Contributions to this project are welcome! If you have any suggestions for improvements or would like to add new features, feel free to submit a pull request.
