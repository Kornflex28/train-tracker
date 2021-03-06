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
            fetch("http://localhost:8080/trainrecords?page=0")
                .then(response => response.json())
                .then((trainrecords) => {
                    for (i = 0; i < trainrecords.length; i++) {
                        trainrecords[i]['departureTime'] = new Date(trainrecords[i]['departureTime']).toLocaleString();
                        trainrecords[i]['arrivalTime'] = new Date(trainrecords[i]['arrivalTime']).toLocaleString();
                    }
                    this.trainrecords = trainrecords;
                })
                .finally(() => (this.loading = false));
        }
    }
});