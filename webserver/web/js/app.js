const requests = new Vue({
    el: '#requests',
    data: {
        requests: [],
    },
    mounted() {
        fetch("localhost:8080/requests")
            .then(response => response.json())
            .then((data) => {
                this.requests = response;
            })
    }
});