import os

from django.conf import settings
from django.test import TestCase, Client


class Exercise2Test(TestCase):
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

    def test_js_content(self):
        """Test that some expected things are in the JS file."""
        with open(os.path.join(settings.BASE_DIR, 'static', 'react-example.js')) as f:
            static_content = f.read()

        self.assertIn('class ClickCounter extends React.Component {', static_content)
        self.assertIn('this.state = { clickCount: 0 };', static_content)
        self.assertIn('return <button onClick={() => this.setState({ clickCount: this.state.clickCount + 1 })}>',
                      static_content)
        self.assertIn('{this.state.clickCount}', static_content)
        self.assertIn('</button>;', static_content)
        self.assertIn('ReactDOM.render(<ClickCounter/>, document.getElementById(\'react_container\'));',
                      static_content)
