const trainrecords = new Vue({
    el: '#trainrecords',
    data: {
        charts: [],
        chartsName: [],
        trainrecords: [],
        trains: [],
        loading: false,
        display: { 'prices': true, 'seats': true },
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
                        datasetsSeats = [];
                        datasetsPrice = [];
                        var dates = trains[train]['recordedTime'];
                        var seats = {};
                        var prices = {};

                        for (i = 0; i < trains[train]['propositions'].length; i++) {
                            for (proposition in trains[train]['propositions'][i]) {
                                if (!Object.keys(seats).includes(proposition)) {
                                    seats[proposition] = [(trains[train]['propositions'][i][proposition]['seats'])];
                                    prices[proposition] = [(trains[train]['propositions'][i][proposition]['amount'])];
                                }
                                else {
                                    //console.log(train,proposition,seats)
                                    seats[proposition].push((trains[train]['propositions'][i][proposition]['seats']));
                                    prices[proposition].push((trains[train]['propositions'][i][proposition]['amount']));
                                }
                            }

                        }

                        var k = 0
                        for (proposition in seats) {
                            var col = 255 * (k / Object.keys(seats).length);
                            datasetsSeats.push({
                                label: proposition,
                                fill: false,
                                data: seats[proposition],
                                backgroundColor: "rgba(255," + col + ",0, 0.5)",
                                borderColor: "rgba(255," + col + ",0, 0.5)",
                                yAxisID: 'y-axis-1',
                            });
                            k += 1;
                        }
                        k = 0;
                        for (proposition in prices) {
                            var col = 255 * (k / Object.keys(seats).length);
                            datasetsPrice.push({
                                label: proposition,
                                fill: false,
                                data: prices[proposition],
                                backgroundColor: "rgba(0," + col + ", 255, 0.5)",
                                borderColor: "rgba(0," + col + ", 255, 0.5)",
                                yAxisID: 'y-axis-1',
                            });
                            k += 1;
                        }
                        spTrain = train.split("_");
                        var title = "De " + spTrain[0].split("(")[0] + "à " + spTrain[2].split("(")[0] + "le " + spTrain[1];
                        var ctxS = document.getElementById(train + "Seats");
                        this.charts.push(new Chart(ctxS, {
                            type: "line",
                            data: {
                                labels: dates,
                                datasets: datasetsSeats,
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
                                            labelString: "Remaining seats",
                                        }
                                    }]
                                },

                                tooltips: {
                                    mode: "index",
                                    intersect: true,
                                },
                                hover: {
                                    mode: "index",
                                    intersect: true,
                                },
                            }
                        }));

                        var ctxP = document.getElementById(train + "Prices");
                        this.charts.push(new Chart(ctxP, {
                            type: "line",
                            data: {
                                labels: dates,
                                datasets: datasetsPrice,
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
                                            labelString: "Price (€)",
                                        },
                                    }]
                                },
                                tooltips: {
                                    mode: "index",
                                    intersect: true,
                                },
                                hover: {
                                    mode: "index",
                                    intersect: true,
                                },
                            }
                        }));
                    }
                })
                .finally(() => (this.loading = false));
        },

        search: function () {
            var input = document.getElementById('searchbar');
            var filter = input.value.toUpperCase();
            var graphs = document.getElementsByTagName('canvas');
            for (i = 0; i < graphs.length; i++) {
                var graph_id = graphs[i].id;
                if (graph_id.toUpperCase().indexOf(filter) > -1) {
                    graphs[i].style.display = "";
                } else {
                    graphs[i].style.display = "none";
                }
            }
        },

        filterMedia: function (className) {
            var graphs = document.getElementsByTagName('canvas');
            var otherClass = (className == 'seats') ? 'prices' : 'seats';

            this.display[className] = !this.display[className];
            for (i = 0; i < graphs.length; i++) {
                var graph_class = graphs[i].className;
                if (graph_class.indexOf(className) > -1) {
                    if (this.display[className]) {
                        graphs[i].parentNode.style.display = "";
                        if (this.display[otherClass]) {
                            graphs[i].parentNode.className = "col-6";
                        }
                        else {
                            graphs[i].parentNode.className = "col";
                        }
                    }
                    else {
                        graphs[i].parentNode.style.display = "none";
                    }
                }

                else {
                    if (this.display[className] && this.display[otherClass]) {
                        graphs[i].parentNode.className = "col-6";
                    }
                    else {
                        graphs[i].parentNode.className = "col";
                    }
                }
            }
        }
    }
});