import os
import re

from django.conf import settings
from django.test import TestCase, Client


class Activity1Test(TestCase):
    def test_cleanup(self):
        """Test that the files, view, etc from the previous exercises have been removed/"""
        self.assertFalse(os.path.exists(os.path.join(settings.BASE_DIR, 'static', 'react-example.js')))
        self.assertFalse(os.path.exists(os.path.join(settings.BASE_DIR, 'templates', 'react-example.html')))

        with self.assertRaises(ImportError):
            from reviews.views import react_example

        c = Client()
        resp = c.get('/react-example/')
        self.assertEquals(resp.status_code, 404)

    def test_template_content(self):
        """Test that the scripts and container have been added to the template."""
        c = Client()
        resp = c.get('/')
        self.assertIn(b'<div id="recent_reviews"></div>', resp.content)
        self.assertIn(b'<script crossorigin src="https://unpkg.com/react@16/umd/react.development.js"></script>',
                      resp.content)
        self.assertIn(
            b'<script crossorigin src="https://unpkg.com/react-dom@16/umd/react-dom.development.js"></script>',
            resp.content)
        self.assertIn(b'<script crossorigin src="https://unpkg.com/babel-standalone@6/babel.min.js"></script>', resp.content)
        self.assertIn(b'<script src="/static/recent-reviews.js" type="text/babel"></script>', resp.content)
        self.assertIn(b'ReactDOM.render(<RecentReviews url="/api/reviews/?limit=6" />,', resp.content)
        self.assertIn(b'document.getElementById(\'recent_reviews\')', resp.content)

    def test_scripts_inside_content_block(self):
        """The script and recent_reviews div should not be in pages other than /"""
        c = Client()
        resp = c.get('/books/')
        self.assertNotIn(b'<div id="recent_reviews"></div>', resp.content)
        self.assertNotIn(b'<script crossorigin src="https://unpkg.com/react@16/umd/react.development.js"></script>',
                         resp.content)
        self.assertNotIn(
            b'<script crossorigin src="https://unpkg.com/react-dom@16/umd/react-dom.development.js"></script>',
            resp.content)
        self.assertNotIn(b'<script crossorigin src="https://unpkg.com/babel-standalone@6/babel.min.js"></script>', resp.content)
        self.assertNotIn(b'<script src="/static/recent-reviews.js" type="text/babel"></script>', resp.content)
        self.assertNotIn(b'ReactDOM.render(<RecentReviews url="/api/reviews/?limit=6" />,', resp.content)
        self.assertNotIn(b'document.getElementById(\'recent_reviews\')', resp.content)

    def test_js_content(self):
        """Test that some expected things are in the JS file."""
        with open(os.path.join(settings.BASE_DIR, 'static', 'recent-reviews.js')) as f:
            static_content = f.read()

        # remove leading/trailing whitespace to make comparison more robust
        s = re.sub(r'^\s+', '', static_content, flags=re.MULTILINE)
        s = re.sub(r'\s+$', '', s, flags=re.MULTILINE)

        review_display_class = """class ReviewDisplay extends React.Component {
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
}"""

        self.assertIn(review_display_class, s)

        recent_reviews_class = """class RecentReviews extends React.Component {
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
}"""
        self.assertIn(recent_reviews_class, s)
