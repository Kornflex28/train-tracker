const trainrecords = new Vue({
    el: '#trainrecords',
    data: {
        chart: null,
        trainrecords: [],
        trains: [],
        dates: [],
        seats: [],
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
                    console.log(Object.keys(trains));

                    dataSets = [];
                    for (var train in trains) {
                        this.dates = trains[train]['recordedTime'];
                        var seats = [];
                        for (i = 0; i < trains[train]['propositions'].length; i++) {
                            seats.push(trains[train]['propositions'][i]["SEMIFLEX"]['seats'])
                            this.seats = seats;
                        }
                        var col = 255 * Math.random();
                        dataSets.push({ 'label': train, fill: false, data: seats, backgroundColor: "rgba(" + col + ", 162, 235, 0.5)", borderColor: "rgba(" + col + ", 162, 235, 0.5)" });
                    }



                    var ctx = document.getElementById("myChart");
                    this.chart = new Chart(ctx, {
                        type: "line",
                        data: {
                            labels: this.dates,
                            datasets: dataSets
                        },
                        options: {
                            title: {
                                display: true,
                                text: "Test"
                            },
                        }
                    });
                })
                .finally(() => (this.loading = false));
        }
    }
});