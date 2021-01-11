class ReviewDisplay extends React.Component {
    constructor(props) {
        super(props);
        this.state = { review: props.review };
    }

    render () {
      const review = this.state.review;

      return <div className="col mb-4">
            <div className="card">
                <div className="card-body">
                    <h5 className="card-title">{ review.book }
                        <strong>({ review.rating })</strong>
                    </h5>
                    <h6 className="card-subtitle mb-2 text-muted">{ review.creator.email }</h6>
                    <p className="card-text">{ review.content }</p>
                </div>
                <div className="card-footer">
                    <a href={'/books/' + review.book_id + '/' } className="card-link">View Book</a>
                </div>
            </div>
        </div>;
    }

}

class RecentReviews extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            reviews: [],
            currentUrl: props.url,
            nextUrl: null,
            previousUrl: null,
            loading: false
        };
    }

    fetchReviews() {
        if (this.state.loading)
            return;
        this.setState( {loading: true} );

        fetch(this.state.currentUrl, {
          method: 'GET',
          headers: {
              Accept: 'application/json'
          }
        }).then((response) => {
          return response.json()
        }).then((data) => {
        this.setState({
                loading: false,
                reviews: data.results,
                nextUrl: data.next,
                previousUrl: data.previous
          })
        })
    }

    componentDidMount() {
        this.fetchReviews()
    }

    loadNext() {
      if (this.state.nextUrl == null)
          return;

        this.state.currentUrl = this.state.nextUrl;
        this.fetchReviews();
    }

    loadPrevious() {
        if (this.state.previousUrl == null)
            return;

        this.state.currentUrl = this.state.previousUrl;
        this.fetchReviews();
    }

    render() {
        if (this.state.loading) {
            return <h5>Loading...</h5>;
        }

        const previousButton = <button
            className="btn btn-secondary"
            onClick={ () => { this.loadPrevious() } }
            disabled={ this.state.previousUrl == null }>
                Previous
        </button>;

        const nextButton = <button
            className="btn btn-secondary float-right"
            onClick={ () => { this.loadNext() } }
            disabled={ this.state.nextUrl == null }>
                Next
        </button>;

        let reviewItems;

        if (this.state.reviews.length === 0) {
            reviewItems = <h5>No reviews to display.</h5>
        } else {
            reviewItems = this.state.reviews.map((review) => {
                return <ReviewDisplay key={review.pk} review={review}/>
            })
        }

        return <div>
            <div className="row row-cols-1 row-cols-sm-2 row-cols-md-3">
                { reviewItems }
            </div>
            <div>
                { previousButton }
                { nextButton }
            </div>
        </div>;
    }
}
