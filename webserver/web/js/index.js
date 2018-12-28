const trainrecords = new Vue({
    el: '#trainrecords',
    data: {
        trainrecords: [],
        loading: false,
    },
    mounted: function () {
        this.formData();
    },

    methods: {
        formData: function () {
            this.loading = true;
            fetch("http://127.0.0.1:8080/trainrecords")
                .then(response => response.json())
                .then((trainrecords) => {
                    for (i = 0; i < trainrecords.length; i++) {
                        console.log(trainrecords[i]['departureTime'], trainrecords[i]['arrivalTime'], trainrecords[i]['recordedTime'])
                        trainrecords[i]['departureTime'] = new Date(trainrecords[i]['departureTime']).toLocaleString();
                        trainrecords[i]['arrivalTime'] = new Date(trainrecords[i]['arrivalTime']).toLocaleString();
                        trainrecords[i]['recordedTime'] = new Date(trainrecords[i]['recordedTime']).toLocaleString();
                    }
                    this.trainrecords = trainrecords;
                })
                .finally(() => (this.loading = false));
        }
    }
});