/**
 * This file contains the functions required to display the burn-down chart and its data for the currently active sprint
 *
 * Last modified: 17-10-2022
 */

google.charts.load('current', {'packages':['corechart']});
google.charts.setOnLoadCallback(drawChart);

/**
 * This function uses the details from the current sprint and its tasks to create an array of data points to be plotted
 * on the burn-down chart
 *
 * @returns {(((Date|number)[]|(Date|number)[])[]|(Date|number)[][])[]} - An array of the data points for both of the
 * lines, actual and ideal remaining story points vs date, for the burn-down chart.
 */
function createChartData() {
    let currentSprint = retrieveLSData(CURRENT_SPRINT_DETAILS);

    console.log(currentSprint.startDate.substring(5,7));
    console.log(currentSprint.endDate.substring(5,7));

    let startDate = new Date(currentSprint.startDate.substring(0,4),(currentSprint.startDate.substring(5,7) - 1),currentSprint.startDate.substring(8,10));  // yyyy-mm-dd
    let endDate = new Date(currentSprint.endDate.substring(0,4), (currentSprint.endDate.substring(5,7) - 1),currentSprint.endDate.substring(8,10));

    console.log(startDate);
    console.log(endDate);

    let totalTime = 0;

    let i = 0;
    while (inventoryTodo.getTask(i) != null) {
        totalTime += Number(inventoryTodo.getTask(i).title._storyPoint);
        i++;
    }
    
    i = 0;
    while (inventoryInprogress.getTask(i) != null) {
        totalTime += Number(inventoryInprogress.getTask(i).title._storyPoint);
        i++;
    }
    
    i = 0;
    while (inventoryCompleted.getTask(i) != null) {
        totalTime += Number(inventoryCompleted.getTask(i).title._storyPoint);
        i++;
    }

    let timeRemaining = totalTime;

    let data1 = [[startDate, totalTime], [endDate, 0]];

    let data2 = [[startDate, totalTime]];


    i = 0;
    while (inventoryCompleted.getTask(i) != null) {
        timeRemaining -= Number(inventoryCompleted.getTask(i).title._storyPoint);
        data2.push([new Date(inventoryCompleted.getTask(i).title._timeCompleted), timeRemaining]);
        i++;
    }
    
    return [data1, data2];
}

/**
 * This function uses Google charts and the create chart data function to create and plot the burn-down chart.
 */
function drawChart() {

    if (retrieveLSData(CURRENT_SPRINT_DETAILS) == null) {
        target = document.getElementById('myChart');
        target.innerHTML = '<h3 style="font-weight: bold; color: white"; text-align: center>No active sprint currently.</h3>';
        return;
    }

    var data1 = new google.visualization.DataTable();
    data1.addColumn('date', 'Date');
    data1.addColumn('number', 'Expected Story Points remaining');
    
    graphData = createChartData();

    data1.addRows(graphData[0]);
    
    var data2 = new google.visualization.DataTable();
    data2.addColumn('date', 'Date');
    data2.addColumn('number', 'Real Story Points remaining');
    
    data2.addRows(graphData[1]);
    
    var joinedData = google.visualization.data.join(data1, data2, 'full', [[0, 0]], [1], [1]);
    
    var chart = new google.visualization.LineChart(document.getElementById('myChart'));
    chart.draw(joinedData, {
        title: 'Sprint Burndown Chart',
        height: 1000,
        width: 1200,
        interpolateNulls: true
    });
}