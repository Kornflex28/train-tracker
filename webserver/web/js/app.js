const trainsrecords = new Vue({
    el: '#trainrecords',
    data: {
        trainrecords: [],
    },
    mounted: function() {
        fetch("http://localhost:8080/trainrecords")
            .then(response => response.json())
            .then((data) => {
                this.trainrecords = data;
                })
    }
});