const e = React.createElement;

class ClickCounter extends React.Component {
    constructor(props) {
        super(props);
        this.state = { clickCount: 0 };
    }

    render() {
        return e(
            'button',
            { onClick: () => this.setState({ clickCount: this.state.clickCount + 1 }) },
            this.state.clickCount
        );
    }
}

ReactDOM.render(e(ClickCounter), document.getElementById('react_container'));
