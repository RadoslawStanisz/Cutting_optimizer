# Project overview

This application is designed for professional woodworkers to automate the cost estimation and nesting optimization of furniture components. It allows users to efficiently manage materials, minimize waste, and generate cutting layouts in SVG format.

### Features

- Automated Cost Estimation: Quickly calculate material quantities for cabinets and kitchen elements.

- Smart Nesting Optimization: Iterates through different algorithms to find the best sheet usage.

- SVG Cutting Layouts: Generates cutting diagrams for precise manufacturing.

- User-Friendly Interface: Built with Streamlit for easy interaction.

- Expandability: Easily add new cabinet types or sheet (board) dimensions to fit specific needs.

### Usage

- Add Cabinets: Enter the dimensions, quantities and type of cabinets in the sidebar.

- Generate Raw materials estimation: Click the `get report` button to get an instant summary.

- Optimize Nesting: The system will automatically select the best cutting layout.

- Create SVG Files: View optimized cutting layouts.

### Screenshots

![image](https://github.com/user-attachments/assets/ef18da18-3f81-4e00-aa23-e33de07237aa)

![image](https://github.com/user-attachments/assets/e31eec4b-11df-4a86-b246-9356dd073a70)


### About Guillotine Algorithms

Guillotine algorithms are a family of cutting algorithms used for material optimization. They work by recursively dividing a sheet into smaller rectangles with straight cuts, similar to how a guillotine slices through paper. These algorithms are particularly useful where minimizing waste is crucial. The application leverages guillotine algorithms in the nesting process to efficiently arrange cabinet components on available sheets. Sometimes due to design requirements it is necessary to cut the material (chipboard, plywood, etc.) in a way that is not optimal. For example, if wood grain direction matter. In these cases user needs to specify it in the sidebar:

![image](https://github.com/user-attachments/assets/c8399008-7fbe-4c97-9354-b012566edf2b) 

Otherwise the app by default may rotate the cabinets' elements focusing only on minimizing waste. There are many different types of guillotine algorithms and there's no best one as the performance depends on the particular input. Therefore, the app iterates over all of them to find the best solution. In this case the best solution is defined as the one with the least number of sheets (boards) used in the process `AND` with the lowest utilization percentage of the last sheet (the remaining/waste part of the sheet can be reused in the future, the bigger it is, the better). The description of the algorithms configurations and input sorting methods can be viewed [here](https://github.com/juj/RectangleBinPack/blob/master/RectangleBinPack.pdf).


### Technologies Used

- Python (Core logic)

- Streamlit (GUI)

- Rectpack (Nesting algorithm)

- SVG Generation (Visualization)
