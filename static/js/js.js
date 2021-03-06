function goToId(id) {
    if (!window.location.hash) window.location = window.location + id;
}

class Pagination {
    constructor(page, maxpage, filter, url) {
        this.page = page;
        this.maxpage = maxpage;
        this.filter = filter;
        this.url = url;
        if (this.page == 1) {
            $("#btn-start").prop( "disabled", true );
            $("#btn-prev").prop( "disabled", true );
        }
        if (this.page == this.maxpage) {
            $("#btn-end").prop( "disabled", true );
            $("#btn-next").prop( "disabled", true );
        }
    }
    start() {
        this.page = 1;
        this.navigate();
    }
    end() {
        this.page = this.maxpage;
        this.navigate();
    }
    next() {
        if(this.page + 1 <= this.maxpage) {
            this.page++;
            this.navigate();
        }
    }
    prev() {
        if(this.page - 1 > 0) {
            this.page--;
            this.navigate();
        }
    }
    navigate() {
        window.location.href = (`${this.url}?page=${this.page}&search=${this.filter}`);
    }
}