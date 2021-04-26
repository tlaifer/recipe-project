import React, {Component} from "react";
import { makeStyles } from '@material-ui/core/styles';
import Grid from '@material-ui/core/Grid';
import Radio from '@material-ui/core/Radio';
import RadioGroup from '@material-ui/core/RadioGroup';
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
const colSize = 20;
/**
 * TODO: replace with DB call to UserTechniques
 */

let intMap = {
  "1": false,
  "2": true,
  "3": null
}

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
      newUserInputName: ''
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
    this.handleIngredientLoad();
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
    axios.post('http://sp21-cs411-13.cs.illinois.edu:5000/api/techniques/', {
      user: this.state.userId,
    }, {
      headers: {
          'Content-Type': 'application/json'
      }
    })
    .then((response) => {
      console.log("SUCCESS", response);
      var techniques = response.data.techniqueArray;
      

      this.setState({ techniques:  techniques});
    }).catch(error => {
      console.log(error)
    });
    return;
  }

  handleIngredientLoad = () => {
    this.ingredientApiCall()
  }

  handleTechniqueLoad = () => {
    this.techniquesApiCall()
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
    }, () => {
      this.handleIngredientLoad();
      this.handleTechniqueLoad();
    });    
  }

  handleTechniqueChange = (event) => {
    let updatedTechniques = this.state.techniques;
    let index = this.state.techniques.findIndex(element => {
      return element.name === event.target.name;
    });
    updatedTechniques[index].value = intMap[event.target.value]

    this.setState({
      techniques: updatedTechniques
    });
  };

  handleIngredientChange = (event, value, reason) => {
    //value will contain the list of currently selected options
    let selectedIngredients = value;

    this.state.ingredients.forEach((ingredient, idx) => {
      if (selectedIngredients.indexOf(ingredient.name) > -1) {
        this.state.ingredients[idx].value = true;
      } else {
        this.state.ingredients[idx].value = false
      }
    });
    this.setState({ ingredients: this.state.ingredients });
  };

  handleIngredientSave = () => {
    axios.post('http://sp21-cs411-13.cs.illinois.edu:5000/api/vetoIngredients/', {
      userId: this.state.userId,
      vetoIngredients: this.state.ingredients.filter(x => x.value == true),
    }, {
      headers: {
          'Content-Type': 'application/json'
      }
    }).then(response => {
      console.log("SUCCESS", response);
    }).catch(error => {
      console.log(error)
    });
  }
  
  handleTechniqueSave = () => {
    axios.put('http://sp21-cs411-13.cs.illinois.edu:5000/api/techniques/', {
      user: this.state.userId,
      techniques: this.state.techniques
    }, {
      headers: {
          'Content-Type': 'application/json'
      }
    }).then(response => {
      console.log("SUCCESS", response);
      this.techniquesApiCall();
    }).catch(error => {
      console.log(error)
    });
  }

  handleSubmitPreferences = () => {
    // First upsert vetoed ingredients
    this.handleIngredientSave()

    // Second upsert user technique selections
    this.handleTechniqueSave()

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
              <tr>
                <th className="technique-header">Cooking Technique</th>
                <th className="technique-header">Yes</th>
                <th className="technique-header">No</th>
                <th className="technique-header">No Preference</th>
              </tr>
            </FormGroup>
            <FormGroup>
              {Array.from(this.state.techniques).map(t=>{
                return (
                  <RadioGroup
                    row aria-label="position"
                    name={t.name}
                    value= { t.value == false ? "1" : t.value == true ? "2" : "3" }
                    onChange={this.handleTechniqueChange}>
                    <div className="technique"> {t.name} </div>
                    <FormControlLabel className="technique"
                      value="1"
                      control={<Radio color="primary" />}
                    />
                    <FormControlLabel className="technique"
                      value="2"
                      control={<Radio color="secondary" />}
                    />
                    <FormControlLabel className="technique"
                      value="3"
                      control={<Radio color="default" />}
                    />
                  </RadioGroup>
                  // <FormControlLabel
                  //   control={<Checkbox
                  //     checked={t.value}
                  //     onChange={this.handleTechniqueChange}
                  //     name={t.name}
                  //   />}
                  //   label={t.name}
                  // />
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
            onChange={(event,value, reason) => this.handleIngredientChange(event,value, reason)}
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