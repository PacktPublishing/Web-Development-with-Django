class ClickCounter extends React.Component {
    constructor(props) {
        super(props);
        this.state = { clickCount: 0 };
    }

    render() {
        return <button onClick={() => this.setState({ clickCount: this.state.clickCount + 1 })}>
           {this.state.clickCount}
        </button>;
    }
}

ReactDOM.render(<ClickCounter/>, document.getElementById('react_container'));