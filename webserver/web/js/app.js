const trainrecords = new Vue({
    el: '#trainrecords',
    data: {
        trainrecords: [],
    },
    mounted: function() {
        fetch("http://localhost:8080/trainrecords")
            .then(response => response.json())
            .then((trainrecords) => {
                for (i=0; i<trainrecords.length; i++ ) {
                    trainrecords[i]['departureTime'] = new Date(trainrecords[i]['departureTime']).toLocaleString() ;
                    trainrecords[i]['arrivalTime'] = new Date(trainrecords[i]['arrivalTime']).toLocaleString() ;
                    trainrecords[i]['recordedTime'] = new Date(trainrecords[i]['recordedTime']).toLocaleString() ;
                }
                this.trainrecords = trainrecords;
                })
    }
});