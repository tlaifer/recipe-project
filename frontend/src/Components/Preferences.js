import React, {Component} from "react";
import { makeStyles } from '@material-ui/core/styles';
import Grid from '@material-ui/core/Grid';
import FormLabel from '@material-ui/core/FormLabel';
import FormControl from '@material-ui/core/FormControl';
import FormGroup from '@material-ui/core/FormGroup';
import FormControlLabel from '@material-ui/core/FormControlLabel';
import Autocomplete from '@material-ui/lab/Autocomplete';
import TextField from '@material-ui/core/TextField';
import Button from '@material-ui/core/Button';
import Checkbox from '@material-ui/core/Checkbox';
import MenuItem from '@material-ui/core/MenuItem';
import Select from '@material-ui/core/Select';
import axios from 'axios';


const submitButtonText = 'Save Changes'
/**
 * TODO: replace with DB call to UserTechniques
 */
let techniquesInit = [
  {
    name: 'tec1',
    value: false
  },
  {
    name: 'tec2',
    value: false
  }
];

/**
 * TODO: replace with DB call to Ingredients & UserIngredients
 */
let ingredients = [
  {
    name: 'tomatoes',
    value: false
  },
  {
    name: 'bread',
    value: false
  }
]

class Preferences extends Component {

  constructor(props) {
    super(props);
    this.state = {
      userId: null,
      techniques: [],
      ingredients: [],
      allUsers: null,
      newUserInputName: '',
      optionsFetched: false
    };
  };

  handleNameChange = (event) => {
    this.setState({
      newUserInputName: event.target.value
    });
  }

  fetchUsers = () => {
    axios.get('http://sp21-cs411-13.cs.illinois.edu:5000/api/users/', {
      headers: {
          'Content-Type': 'application/json'
      }
    })
    .then(response => {
      this.setState({ allUsers: response.data});
      console.log("got users: " + JSON.stringify(this.allUsers) + JSON.stringify(response.data));
    })
    .catch(e => {
      console.log(e);
      this.setState({...this.state});
    });
  };

  componentDidMount() {
    this.fetchUsers();
  };

  ingredientApiCall = () => { /** TODO: this should probably be props rather than state */
    axios.get('http://sp21-cs411-13.cs.illinois.edu:5000/api/ingredients/')
    .then((response) => {
      console.log("SUCCESS", response);
      this.setState({ ingredients: response.data.ingredientArray });
    }).catch(error => {
      console.log(error)
    });
    return;
  }

  techniquesApiCall = () => { /** TODO: this should probably be props rather than state */
    axios.get('http://sp21-cs411-13.cs.illinois.edu:5000/api/techniques/')
    .then((response) => {
      console.log("SUCCESS", response);
      this.setState({ techniques: response.data.techniqueArray });
    }).catch(error => {
      console.log(error)
    });
    return;
  }

  handleIngredientLoad = () => {
    if (this.state.optionsFetched === false) {
      this.ingredientApiCall()
      this.setState({ optionsFetched: true });
    }
  }

  handleTechniqueLoad = () => {
    if (this.state.optionsFetched === false) {
      this.techniquesApiCall()
      this.setState({ optionsFetched: true });
    }
  }

  handleDeleteUser = () => {
    axios.delete('http://sp21-cs411-13.cs.illinois.edu:5000/api/user/' + this.state.userId)
    .then(response => {
      console.log("SUCCESS", response);
      this.fetchUsers();
    })
    .catch(error => {
      console.log(error)
    });
  }


  handleCreateUser = () => {
    axios.put('http://sp21-cs411-13.cs.illinois.edu:5000/api/user/', {
      name: this.state.newUserInputName
    }, {
      headers: {
          'Content-Type': 'application/json'
      }
    }).then(response => {
      console.log("SUCCESS", response);
      this.fetchUsers();
      this.state.newUserInputName = null;
    }).catch(error => {
      console.log(error)
    });
  }

  handleUserChage = (event) => {
    this.setState({
      userId: event.target.value
    });
    /**
     * TODO: fetch user prefs
     */
    this.render();
  }

  handleTechniqueChange = (event) => {
    let index = this.state.techniques.findIndex(element => {
      return element.name === event.target.name;
    });
    this.state.techniques[index].value = event.target.checked

    this.setState({
      techniques: this.state.techniques
    });
  };

  handleIngredientChange = (event, value, reason) => {
    //value will contain the list of currently selected options
    let selectedIngredients = value;

    this.state.ingredients.forEach(ingredient => {
      if (selectedIngredients.indexOf(this.state.ingredients.name) > -1) {
        this.state.ingredients.value = true;
      } else {
        this.state.ingredients.value = false
      }
    });
    this.setState({ ingredients: this.state.ingredients });
  };

  handleSubmitPreferences = () => {
    /**
     * TODO: submit user preferences to server
     */
    return;
  };

  render() {
    this.handleIngredientLoad()
    this.handleTechniqueLoad()
    console.log('render called');
    return (
      <div className="body">
        <div className="user-inputs">
          <Grid container spacing={3}>
            <Grid item xs>Choose your user
              <Select
                labelId="select-user"
                value={this.userId}
                onChange={this.handleUserChage}
              >
                {this.state.allUsers && this.state.allUsers.map(u => {
                  return (<MenuItem value={u.id}>{u.name}</MenuItem>)
                })}
              </Select>
              <Button variant="contained" color="default" onClick={this.handleDeleteUser}>delete user</Button>
            </Grid>
            <Grid item xs>
              <TextField id="user-input" label="user name" variant="outlined" type="search" value={this.newUserInputName} onChange={this.handleNameChange}/>
              <Button variant="contained" color="default" onClick={this.handleCreateUser}>create user</Button>
            </Grid>
          </Grid>
        </div>
        <Grid container spacing={3}>
          <FormControl component="fieldset">
            <FormLabel component="legend">What can you do in the kitchen?</FormLabel>
            <FormGroup>
              {Array.from(this.state.techniques).map(t=>{
                return (
                  <FormControlLabel
                    control={<Checkbox
                      checked={t.value}
                      onChange={this.handleTechniqueChange}
                      name={t.name}
                    />}
                    label={t.name}
                  />
                )
              })}
            </FormGroup>
          </FormControl>
        </Grid>
        <Grid container spacing={3}>
          <Autocomplete className="body"
            multiple
            id="tags-standard"
            style={{ alignContent: "left" }}
            options={Array.from(this.state.ingredients).map(ingredient => ingredient.name)}
            //defaultValue={[state.ingredients[0].name]}
            getOptionLabel={(option) => option}
            onChange={this.handleIngredientChange}
            renderInput={(params) => (
              <TextField
                {...params}
                variant="standard"
                placeholder="I won't eat..."
              />
            )}
          />
        </Grid>
        <Grid container spacing={3}>
          <Grid item xs>
          </Grid>
          <Grid item xs>
          </Grid>
          <Grid item xs>
            <Button variant="contained" color="primary" onClick={this.handleSubmitPreferences}>{submitButtonText}</Button>
          </Grid>
        </Grid>
      </div>
    );
  }
}

export default Preferences;