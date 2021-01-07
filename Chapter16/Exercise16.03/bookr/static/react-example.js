class ClickCounter extends React.Component {
    constructor(props) {
        super(props);
        this.state = { clickCount: 0, name: props.name, target: props.target };
    }

    render() {
        if (this.state.clickCount === this.state.target) {
            return <span>Well done, {this.state.name}!</span>;
        }

        return <button onClick={() => this.setState({ clickCount: this.state.clickCount + 1 })}>
           {this.state.clickCount}
        </button>;
    }
}