import os

from django.conf import settings
from django.test import TestCase, Client


class Exercise4Test(TestCase):
    def test_view_and_template(self):
        """Test that the view, URLs and template are set up properly by checking the contents of the response."""
        c = Client()
        resp = c.get('/react-example/')
        self.assertIn(b'<div id="react_container"></div>', resp.content)
        self.assertIn(b'<script crossorigin src="https://unpkg.com/react@16/umd/react.development.js"></script>',
                      resp.content)
        self.assertIn(
            b'<script crossorigin src="https://unpkg.com/react-dom@16/umd/react-dom.development.js"></script>',
            resp.content)
        self.assertIn(b'<script crossorigin src="https://unpkg.com/babel-standalone@6/babel.min.js"></script>', resp.content)
        self.assertIn(b'<script src="/static/react-example.js" type="text/babel"></script>', resp.content)
        self.assertIn(b'<script type="text/babel">', resp.content)
        self.assertIn(b'ReactDOM.render(<BookDisplay url="/api/books/" />,', resp.content)

    def test_js_content(self):
        """Test that some expected things are in the JS file."""
        with open(os.path.join(settings.BASE_DIR, 'static', 'react-example.js')) as f:
            static_content = f.read()

        self.assertIn('class BookDisplay extends React.Component {', static_content)
        self.assertIn('this.state = { books: [], url: props.url, fetchInProgress: false };', static_content)
        self.assertIn('doFetch() {', static_content)
        self.assertIn('if (this.state.fetchInProgress)', static_content)
        self.assertIn('fetch(this.state.url, {', static_content)
        self.assertIn(').then((response) => {', static_content)
        self.assertIn('return response.json();', static_content)
        self.assertIn('}).then((data) => {', static_content)
        self.assertIn('this.setState({ fetchInProgress: false, books: data })', static_content)
        self.assertIn('const bookListItems = this.state.books.map((book) => {', static_content)
        self.assertIn('return <li key={ book.pk }>{ book.title }</li>;', static_content)
        self.assertIn('const buttonText = this.state.fetchInProgress  ? \'Fetch in Progress\' : \'Fetch\';',
                      static_content)
        self.assertIn('return <div>', static_content)
        self.assertIn('<ul>{ bookListItems }</ul>', static_content)
        self.assertIn('<button onClick={ () => this.doFetch() } disabled={ this.state.fetchInProgress }>',
                      static_content)
        self.assertIn('{buttonText}', static_content)
        self.assertNotIn('ReactDOM.render', static_content)
