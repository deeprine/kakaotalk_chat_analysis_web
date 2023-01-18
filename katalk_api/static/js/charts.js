google.charts.load('current', {'packages':['corechart', 'bar', 'table', 'line']});
// google.charts.load('current', {'packages': ['corechart', 'bar']});
google.charts.setOnLoadCallback(user_day_1);
google.charts.setOnLoadCallback(user_day_2);
google.charts.setOnLoadCallback(user_day_3);
google.charts.setOnLoadCallback(user_day_4);
google.charts.setOnLoadCallback(day_1);
google.charts.setOnLoadCallback(day_2);
google.charts.setOnLoadCallback(day_3);
google.charts.setOnLoadCallback(day_4);
google.charts.setOnLoadCallback(ratio_drawChart);
google.charts.setOnLoadCallback(pic_drawChart);
google.charts.setOnLoadCallback(emo_drawChart);
google.charts.setOnLoadCallback(speech_1_chart);
google.charts.setOnLoadCallback(speech_2_chart);
google.charts.setOnLoadCallback(topic_1_chart);
google.charts.setOnLoadCallback(topic_2_chart);
google.charts.setOnLoadCallback(recommend_chart);

let ratio = result_obj.ratio_katalk_dict;
let day = result_obj.day_dict;
let day_continue = result_obj.continue_dict;
let ratio_pic = result_obj.ratio_pic_dict;
let ratio_emo = result_obj.ratio_emo_dict;
let topic = result_obj.topic_dict;
let speech = result_obj.speech_dict;
let user_unique = users;
let user_1 = user_unique[0];
let user_2 = user_unique[1];
let user_day = result_obj.user_day_dict;

// if (user_unique.length <= 2) {
//     topic_user_1.innerHTML = "<h4>" + user_1 + '님의 대화주제 ' + "</h4>" + topic[user_1 + '_주제']
//     topic_user_2.innerHTML = "<h4>" + user_2 + '님의 대화주제 ' + "</h4>" + topic[user_2 + '_주제']
//     topic_recommend.innerHTML = "<h4>" + '우리에게 맞는 추천주제 '+ "</h4>"  + topic['주제추천']
// }

day_connection.innerHTML = day_continue['continue'][0] + ' 부터 ' + day_continue['continue'][1] + ' 까지 ' + '<br>' + '<h4>' + day_continue['continue'][2] + ' 일' + '</h4>' + '이어졌어요.'
day_max_connection.innerHTML = day_continue['max_continue'][0] + ' 부터 ' + day_continue['max_continue'][1] + ' 까지 ' + '<br>' + '<h4>' + day_continue['max_continue'][2] + ' 일' + '</h4>' + '대화하지 않았어요.'

function ratio_drawChart() {

    ratio_arr = [['Task', 'Hours per Day']];
    for (i=0; i<user_unique.length; i++){
        ratio_arr.push([user_unique[i], ratio[user_unique[i]]])
    }

    var data = google.visualization.arrayToDataTable(
        ratio_arr
    );

    var options = {
        title: '카톡대화 비율',
        is3D: true,
        width: '100%',
        chartArea:{width:'100%', height:'85%'}
    };

    var chart = new google.visualization.PieChart(document.getElementById('ratio_piechart'));

    chart.draw(data, options);
}

function emo_drawChart() {

    emo_arr = [['Task', 'Hours per Day']];
    for (i=0; i<user_unique.length; i++){
        emo_arr.push([user_unique[i], ratio_emo[user_unique[i] + '_이모티콘']])
    }

    var data = google.visualization.arrayToDataTable(
        emo_arr
    );

    var options = {
        title: '카톡이모티콘 비율',
        is3D: true,
        width: '100%',
        chartArea:{width:'100%', height:'85%'}
    };
    
    var chart = new google.visualization.PieChart(document.getElementById('emo_piechart'));

    chart.draw(data, options);
}

function pic_drawChart() {
    
    pic_arr = [['Task', 'Hours per Day']];
    for (i=0; i<user_unique.length; i++){
        pic_arr.push([user_unique[i], ratio_pic[user_unique[i] + '_사진']])
    }
    
    var data = google.visualization.arrayToDataTable(
        pic_arr
    );

    var options = {
        title: '카톡사진 비율',
        is3D: true,
        width: '100%',
        chartArea:{width:'100%', height:'85%'}
    };

    var chart = new google.visualization.PieChart(document.getElementById('pic_piechart'));

    chart.draw(data, options);
}

function day_1() {
    let day_list = [['요일', '대화 갯수', { role: 'style' }]];

    for(d=0; d<day.요일.length; d++){
        let day_result = [day.요일[d], day.요일_num[d], 'silver'];
        day_list.push(day_result);
    }

    var data = google.visualization.arrayToDataTable(
         day_list
    );

    var view = new google.visualization.DataView(data);
    view.setColumns([0, 1,
                       { calc: "stringify",
                         sourceColumn: 1,
                         type: "string",
                         role: "annotation" },
                       2]);

    var options = {
        title: '요일',
        is3D: true,
        width: '100%',
        bar: {groupWidth: "95%"},
        colors: ['silver'],
        chartArea:{width:'85%'},
        legend:{position: 'bottom'}
    };
    var materialChart = new google.visualization.ColumnChart(document.getElementById('day_1_div'));
    materialChart.draw(view, options);
}

function day_2() {
    let day_list = [['년월', '대화 갯수', { role: 'style' }]];

    for(d=0; d<day.년월.length; d++){
        let day_result = [day.년월[d], day.년월_num[d], 'silver'];
        day_list.push(day_result);
    }

    var data = google.visualization.arrayToDataTable(
         day_list
    );

    var view = new google.visualization.DataView(data);
    view.setColumns([0, 1,
                       { calc: "stringify",
                         sourceColumn: 1,
                         type: "string",
                         role: "annotation" },
                       2]);

    var options = {
        title: '년월',
        is3D: true,
        width: '100%',
        bar: {groupWidth: "85%"},
        colors: ['silver'],
        chartArea:{width:'85%'},
        legend:{position: 'bottom'}
    };
    var materialChart = new google.visualization.ColumnChart(document.getElementById('day_2_div'));
    materialChart.draw(view, options);
}

function day_3() {
    let day_list = [['년월일', '대화 갯수', { role: 'style' }]];

    for(d=0; d<day.년월일.length; d++){
        let day_result = [day.년월일[d], day.년월일_num[d], 'silver'];
        day_list.push(day_result);
    }

    var data = google.visualization.arrayToDataTable(
         day_list
    );

    var view = new google.visualization.DataView(data);
      view.setColumns([0, 1,
                       { calc: "stringify",
                         sourceColumn: 1,
                         type: "string",
                         role: "annotation" },
                       2]);

    var options = {
        title: '년월일',
        is3D: true,
        width: '100%',
        bar: {groupWidth: "85%"},
        colors: ['silver'],
        chartArea:{width:'85%'},
        legend:{position: 'bottom'}
    };
    var materialChart = new google.visualization.ColumnChart(document.getElementById('day_3_div'));
    materialChart.draw(view, options);
}

function day_4() {
    let day_list = [['시간', '대화 갯수', { role: 'style' }]];

    for(d=0; d<day.시간.length; d++){
        let day_result = [day.시간[d], day.시간_num[d], 'silver'];
        day_list.push(day_result);
    }

    var data = google.visualization.arrayToDataTable(
         day_list
    );

    var view = new google.visualization.DataView(data);
      view.setColumns([0, 1,
                       { calc: "stringify",
                         sourceColumn: 1,
                         type: "string",
                         role: "annotation" },
                       2]);

    var options = {
        title: '시간',
        is3D: false,
        width: '100%',
        bar: {groupWidth: "75%"},
        colors: ['silver'],
        chartArea:{width:'85%'},
        legend:{position: 'bottom'}
    };

    var materialChart = new google.visualization.ColumnChart(document.getElementById('day_4_div'));
    materialChart.draw(view, options);
}


// test
function user_day_1() {
    let columns = [];
    let results = [];

    columns.push('time');
    for(u=0; u<user_unique.length; u++){
        columns.push(user_unique[u])
    }
    results.push(columns);

    for(d=0; d<user_day['total_시간'].length; d++){
        let day_result = [];
        day_result.push(user_day['total_시간'][d])
        
        for(u=0; u<user_unique.length; u++){
            if(user_day[user_unique[u] + '_시간'].includes(user_day['total_시간'][d])){
                let user_time_index = user_day[user_unique[u] + '_시간'].indexOf(user_day['total_시간'][d])
                day_result.push(user_day[user_unique[u] + '_시간_num'][user_time_index])
            }else{
                day_result.push(0)
            }
        }
        results.push(day_result);
    }

    var data = google.visualization.arrayToDataTable(results);

    var options = {
        title: '사용자 시간별 대화수',
        is3D: false,
        width: '100%',
        chartArea:{width:'85%'},
        legend:{position: 'bottom'}
    };

    var chart = new google.visualization.LineChart(document.getElementById('user_day_1'));

    chart.draw(data, options);
}

function user_day_2() {
    let columns = [];
    let results = [];

    columns.push('요일');
    for(u=0; u<user_unique.length; u++){
        columns.push(user_unique[u])
    }
    results.push(columns);

    for(d=0; d<user_day['total_요일'].length; d++){
        let day_result = [];
        day_result.push(user_day['total_요일'][d])

        for(u=0; u<user_unique.length; u++){
            if(user_day[user_unique[u] + '_요일'].includes(user_day['total_요일'][d])){
                let user_time_index = user_day[user_unique[u] + '_요일'].indexOf(user_day['total_요일'][d])
                day_result.push(user_day[user_unique[u] + '_요일_num'][user_time_index])
            }else{
                day_result.push(0)
            }
        }
        results.push(day_result);
    }

    var data = google.visualization.arrayToDataTable(results);

    var options = {
        title: '사용자 요일별 대화수',
        is3D: false,
        width: '100%',
        chartArea:{width:'85%'},
        legend:{position: 'bottom'}
    };

    var chart = new google.visualization.LineChart(document.getElementById('user_day_2'));

    chart.draw(data, options);
}

function user_day_3() {
    let columns = [];
    let results = [];

    columns.push('년도');
    for(u=0; u<user_unique.length; u++){
        columns.push(user_unique[u])
    }
    results.push(columns);

    for(d=0; d<user_day['total_년'].length; d++){
        let day_result = [];
        day_result.push(user_day['total_년'][d])

        for(u=0; u<user_unique.length; u++){
            if(user_day[user_unique[u] + '_년'].includes(user_day['total_년'][d])){
                let user_time_index = user_day[user_unique[u] + '_년'].indexOf(user_day['total_년'][d])
                day_result.push(user_day[user_unique[u] + '_년_num'][user_time_index])
            }else{
                day_result.push(0)
            }
        }
        results.push(day_result);
    }

    var data = google.visualization.arrayToDataTable(results);

    var options = {
        title: '사용자 년도별 대화수',
        is3D: false,
        width: '100%',
        chartArea:{width:'85%'},
        legend:{position: 'bottom'}
    };

    var chart = new google.visualization.LineChart(document.getElementById('user_day_3'));

    chart.draw(data, options);
}

function user_day_4() {
    let columns = [];
    let results = [];

    columns.push('년월');
    for(u=0; u<user_unique.length; u++){
        columns.push(user_unique[u])
    }
    results.push(columns);

    for(d=0; d<user_day['total_년월'].length; d++){
        let day_result = [];
        day_result.push(user_day['total_년월'][d])

        for(u=0; u<user_unique.length; u++){
            if(user_day[user_unique[u] + '_년월'].includes(user_day['total_년월'][d])){
                let user_time_index = user_day[user_unique[u] + '_년월'].indexOf(user_day['total_년월'][d])
                day_result.push(user_day[user_unique[u] + '_년월_num'][user_time_index])
            }else{
                day_result.push(0)
            }
        }
        results.push(day_result);
    }

    var data = google.visualization.arrayToDataTable(results);

    var options = {
        title: '사용자 년도월별 대화수',
        is3D: false,
        width: '100%',
        chartArea:{width:'85%'},
        legend:{position: 'bottom'}
    };

    var chart = new google.visualization.LineChart(document.getElementById('user_day_4'));

    chart.draw(data, options);
}

// test

function speech_1_chart() {
    var cssClassNames = {
        'headerRow': 'italic-darkblue-font large-font bold-font',
        'tableRow': 'italic-darkblue-font',
        'oddTableRow': 'italic-darkblue-font',
        'selectedTableRow': 'orange-background large-font',
        'hoverTableRow': '',
        'headerCell': 'gold-border',
        'tableCell': '',
        'rowNumberCell': 'underline-blue-font'};

    let speech_arr = speech[user_1 + '_말투']
    // console.log('테스트',speech_arr)
    // speech_arr.unshift(['말투', '갯수']);

    var data = new google.visualization.DataTable();
    data.addColumn('string', user_1 + '의 말투');
    data.addColumn('number', '사용횟수');
    data.addRows(speech_arr);

    var table = new google.visualization.Table(document.getElementById('speech_1_div'));

    table.draw(data, {showRowNumber: true, width: '100%', height: '100%', 'allowHtml': true, 'cssClassNames': cssClassNames});

}

function speech_2_chart() {
    var cssClassNames = {
        'headerRow': 'italic-purple-font large-font bold-font',
        'tableRow': 'italic-purple-font',
        'oddTableRow': 'italic-purple-font',
        'selectedTableRow': 'orange-background large-font',
        'hoverTableRow': '',
        'headerCell': 'gold-border',
        'tableCell': '',
        'rowNumberCell': 'underline-blue-font'};

    let speech_arr = speech[user_2 + '_말투']

        var data = new google.visualization.DataTable();
    data.addColumn('string', user_2 + '의 말투');
    data.addColumn('number', '사용횟수');
    data.addRows(speech_arr);

    var table = new google.visualization.Table(document.getElementById('speech_2_div'));

    table.draw(data, {showRowNumber: true, width: '100%', height: '100%', 'allowHtml': true, 'cssClassNames': cssClassNames});
}

function topic_1_chart() {
    var cssClassNames = {
        'headerRow': 'italic-darkblue-font large-font bold-font',
        'tableRow': 'italic-darkblue-font',
        'oddTableRow': 'italic-darkblue-font',
        'selectedTableRow': 'orange-background large-font',
        'hoverTableRow': '',
        'headerCell': 'gold-border',
        'tableCell': '',
        'rowNumberCell': 'underline-blue-font'};

    let topic_arr = topic[user_1 + '_주제']

    let topic_arr_list = [];
    for(i=0; i<topic_arr.length; i++){
        topic_arr_list.push([topic_arr[i]])
    }

    var data = new google.visualization.DataTable();
    data.addColumn('string', user_1 + '의 주제');
    data.addRows(topic_arr_list);

    var table = new google.visualization.Table(document.getElementById('topic_1_div'));

    table.draw(data, {showRowNumber: true, width: '100%', height: '100%', 'allowHtml': true, 'cssClassNames': cssClassNames});
}

function topic_2_chart() {
    var cssClassNames = {
        'headerRow': 'italic-purple-font large-font bold-font',
        'tableRow': 'italic-purple-font',
        'oddTableRow': 'italic-purple-font',
        'selectedTableRow': 'orange-background large-font',
        'hoverTableRow': '',
        'headerCell': 'gold-border',
        'tableCell': '',
        'rowNumberCell': 'underline-blue-font'};

    let topic_arr = topic[user_2 + '_주제']

    let topic_arr_list = [];
    for(i=0; i<topic_arr.length; i++){
        topic_arr_list.push([topic_arr[i]])
    }

    var data = new google.visualization.DataTable();
    data.addColumn('string', user_2 + '의 대화주제');
    data.addRows(topic_arr_list);

    var table = new google.visualization.Table(document.getElementById('topic_2_div'));

    table.draw(data, {showRowNumber: true, width: '100%', height: '100%', 'allowHtml': true, 'cssClassNames': cssClassNames});
}

function recommend_chart() {
    var cssClassNames = {
        'headerRow': 'italic-darkblue-font large-font bold-font',
        'tableRow': 'italic-darkblue-font',
        'oddTableRow': 'italic-darkblue-font',
        'selectedTableRow': 'orange-background large-font',
        'hoverTableRow': '',
        'headerCell': 'gold-border',
        'tableCell': '',
        'rowNumberCell': 'underline-blue-font'};

    let recommend_arr = topic['주제추천']

    let recommend_arr_list = [];
    if (recommend_arr.length == 1) {
        for (i = 0; i < recommend_arr[0].length; i++) {
            recommend_arr_list.push([recommend_arr[0][i]])
        }
    }else{
        for (i = 0; i < recommend_arr.length; i++) {
            recommend_arr_list.push([recommend_arr[i]])
        }
    }

    var data = new google.visualization.DataTable();
    data.addColumn('string', '추천 대화주제');
    data.addRows(recommend_arr_list);

    var table = new google.visualization.Table(document.getElementById('recommend_div'));

    table.draw(data, {showRowNumber: true, width: '100%', height: '100%', 'allowHtml': true, 'cssClassNames': cssClassNames});
}