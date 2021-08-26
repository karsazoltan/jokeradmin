function goToId() {
    if (!window.location.hash) window.location = window.location + '#form';
}

class Pagination {
    constructor(page, maxpage, filter, url) {
        this.page = page;
        this.maxpage = maxpage;
        this.filter = filter;
        this.url = url;
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