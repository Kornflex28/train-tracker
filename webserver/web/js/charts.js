const trainrecords = new Vue({
    el: '#trainrecords',
    data: {
        charts: [],
        chartsName: [],
        trainrecords: [],
        trains: [],
        loading: false,
    },
    mounted: function () {
        this.formData();
    },

    methods: {
        formData: function () {
            this.loading = true;
            fetch("http://localhost:8080/trainrecords")
                .then(response => response.json())
                .then((trainrecords) => {
                    for (i = 0; i < trainrecords.length; i++) {
                        trainrecords[i]['departureTime'] = new Date(trainrecords[i]['departureTime']).toLocaleString();
                        trainrecords[i]['arrivalTime'] = new Date(trainrecords[i]['arrivalTime']).toLocaleString();
                        trainrecords[i]['recordedTime'] = new Date(trainrecords[i]['recordedTime']).toLocaleString();
                        trainrecords[i]['name'] = trainrecords[i]['origin'] + "_" + trainrecords[i]['departureTime'] + "_" + trainrecords[i]['destination'];
                    }
                    this.trainrecords = trainrecords;

                    var trains = {};
                    for (i = 0; i < trainrecords.length; i++) {
                        var train = trainrecords[i]['name'];
                        if (!Object.keys(trains).includes(train)) {
                            trains[train] = { 'recordedTime': [trainrecords[i]['recordedTime']], 'propositions': [trainrecords[i]['propositions']] };
                        }
                        else {
                            trains[train]['recordedTime'].push(trainrecords[i]['recordedTime']);
                            trains[train]['propositions'].push(trainrecords[i]['propositions']);
                        }
                    }
                    this.trains = trains;
                    this.chartsName = Object.keys(trains);
                    return trains
                })
                .then((trains) => {
                    for (var train in trains) {
                        dataSets = [];
                        var dates = trains[train]['recordedTime'];
                        var seats = {};
                        var prices = {};

                        for (i = 0; i < trains[train]['propositions'].length; i++) {
                            for (proposition in trains[train]['propositions'][i]) {
                                if (!i) {
                                    seats[proposition] = [(trains[train]['propositions'][i][proposition]['seats'])];
                                    prices[proposition] = [(trains[train]['propositions'][i][proposition]['amount'])];
                                }
                                else {
                                    seats[proposition].push((trains[train]['propositions'][i][proposition]['seats']));
                                    prices[proposition].push((trains[train]['propositions'][i][proposition]['amount']));
                                }
                            }

                        }

                        var k = 0
                        for (proposition in seats) {
                            var col = 255 * (k / Object.keys(seats).length);
                            dataSets.push({
                                label: proposition,
                                fill: false,
                                data: seats[proposition],
                                backgroundColor: "rgba(255," + col + ",0, 0.5)",
                                borderColor: "rgba(255," + col + ",0, 0.5)",
                                yAxisID: 'y-axis-1'
                            });
                            // dataSets.push({
                            //     label: "Prices " + proposition,
                            //     fill: false,
                            //     data: prices[proposition],
                            //     backgroundColor: "rgba(255,0," + col + ", 0.5)",
                            //     borderColor: "rgba(255,0," + col + ", 0.5)",
                            //     yAxisID: 'y-axis-2'
                            // });
                            k += 1;
                        }
                        spTrain = train.split("_");
                        var title = "De " + spTrain[0] + " à " + spTrain[2] + " le " + spTrain[1];
                        var ctx = document.getElementById(train);
                        this.charts.push(new Chart(ctx, {
                            type: "line",
                            data: {
                                labels: dates,
                                datasets: dataSets
                            },
                            options: {
                                title: {
                                    display: true,
                                    text: title,
                                    fontSize: 14,
                                },

                                scales: {
                                    yAxes: [{
                                        type: 'linear',
                                        display: true,
                                        position: 'left',
                                        id: 'y-axis-1',
                                        scaleLabel: {
                                            display: true,
                                            labelString: "Remaining seats"
                                        }
                                    }
                                    //     , {
                                    //     type: 'linear',
                                    //     display: true,
                                    //     position: 'right',
                                    //     id: 'y-axis-2',
                                    //     scaleLabel: {
                                    //         display: true,
                                    //         labelString: "Prices (€)"
                                    //     }
                                    // }
                                    ]
                                },
                            }
                        }));
                    }
                })
                .finally(() => (this.loading = false));
        }
    }
});