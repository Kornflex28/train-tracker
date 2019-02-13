const stations = new Vue({
    el: '#stations',
    data: {
        stations: [],
        loading: false,
    },
    mounted: function () {
        this.formData();
    },

    methods: {
        formData: function () {
            this.loading = true;
            fetch("http://localhost:8080/stations")
                .then(response => response.json())
                .then((stations) => this.stations = stations)
                .finally(() => (this.loading = false));
        },
        search: function () {
            var input = document.getElementById('searchbar');
            var filter = input.value.toUpperCase();
            this.searchStation(filter);
        },

        searchStation: function (searchItem) {
            this.loading = true;
            fetch("http://localhost:8080/stations?name=" + searchItem)
                .then(response => response.json())
                .then((stations) => this.stations = stations)
                .finally(() => (this.loading = false));
        }
    }
});