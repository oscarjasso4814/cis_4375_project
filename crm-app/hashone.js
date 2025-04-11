import bcrypt from "bcrypt";

const hashOne = async () => {
  const password = "password123";
  const hashed = await bcrypt.hash(password, 12);

  console.log("Plain:", password);
  console.log("Hashed:", hashed);
};

hashOne();
