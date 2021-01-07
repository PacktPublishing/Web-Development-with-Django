import os

from django.conf import settings
from django.test import TestCase, Client


class Exercise3Test(TestCase):
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
        self.assertIn(b'let name = "Ben";', resp.content)
        self.assertIn(b'let target = 5;', resp.content)
        self.assertIn(b'ReactDOM.render(<ClickCounter name={ name } target={ target }/>,', resp.content)

    def test_js_content(self):
        """Test that some expected things are in the JS file."""
        with open(os.path.join(settings.BASE_DIR, 'static', 'react-example.js')) as f:
            static_content = f.read()

        self.assertIn('class ClickCounter extends React.Component {', static_content)
        self.assertIn('this.state = { clickCount: 0, name: props.name, target: props.target };', static_content)
        self.assertIn('if (this.state.clickCount === this.state.target) {', static_content)
        self.assertIn('return <span>Well done, {this.state.name}!</span>;', static_content)
        self.assertIn('return <button onClick={() => this.setState({ clickCount: this.state.clickCount + 1 })}>',
                      static_content)
        self.assertIn('{this.state.clickCount}', static_content)
        self.assertIn('</button>;', static_content)
        self.assertNotIn('ReactDOM.render', static_content)
