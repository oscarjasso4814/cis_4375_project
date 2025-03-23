import axios from "axios";

// This function has been moved to the actual view it's used in. For some reason, axios doesn't respond fast enough to use return.
// Use as a reference if needed.
// export const getRepName = async (repid) => {
//   axios.get('http://127.0.0.1:5000/api/rep/' + repid + '/name')
//   .then((response) => {
//     let representative = response.data[0].FirstName + " " + response.data[0].LastName
//     console.log(representative);
//     return representative;
//   });
// }