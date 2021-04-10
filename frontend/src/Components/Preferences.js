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
let techniques = [
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
      techniques: techniques,
      ingredients: ingredients,
      allUsers: null,
      newUserInputName: ''
    };
  };

  handleNameChange = (event) => {
    this.setState({
      newUserInputName: event.target.value
    });
  }

  fetchUsers = () => {
    axios.get('http://localhost:5000/api/users/', {
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

  handleDeleteUser = () => {
    axios.delete('http://localhost:5000/api/user/' + this.state.userId)
    .then(response => {
      console.log("SUCCESS", response);
      this.fetchUsers();
    })
    .catch(error => {
      console.log(error)
    });
  }


  handleCreateUser = () => {
    axios.put('http://localhost:5000/api/user/', {
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
    let index = techniques.findIndex(element => {
      return element.name === event.target.name;
    });
    techniques[index].value = event.target.checked

    this.setState({
      techniques: techniques
    });
  };

  handleIngredientChange = (event, value, reason) => {
    //value will contain the list of currently selected options
    let selectedIngredients = value;

    ingredients.forEach(ingredient => {
      if (selectedIngredients.indexOf(ingredient.name) > -1) {
        ingredient.value = true;
      } else {
        ingredient.value = false
      }
    });
    this.setState({ ingredients: ingredients });
  };

  handleSubmitPreferences = () => {
    /**
     * TODO: submit user preferences to server
     */
    return;
  };

  render() {
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
              {this.state.techniques.map(t=>{
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
            options={this.state.ingredients.map(ingredient => ingredient.name)}
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