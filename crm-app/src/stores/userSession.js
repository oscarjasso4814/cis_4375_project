import { ref } from "vue";

export const user = ref(JSON.parse(sessionStorage.getItem("user")) || null);
export const totalWorkedTime = ref(null);


export const setUser = (userData) => {
  user.value = userData;
  sessionStorage.setItem("user", JSON.stringify(userData));
};

export const clearUser = () => {
  user.value = null;
  totalWorkedTime.value = null;
  sessionStorage.removeItem("user");
  sessionStorage.removeItem("reps_id");
};
