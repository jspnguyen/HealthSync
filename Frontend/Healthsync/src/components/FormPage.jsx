import Sidebar from "./Sidebar";
import { useForm } from "react-hook-form";

function FormPage() {
  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm();
  const onSubmit = async (data) => {
    try {
      const response = await fetch("http://0.0.0.0:8080/walkin/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          description: data.message,
        }),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! Status: ${response.status}`);
      }

      const result = await response.json();
      console.log("Response received:", result);
    } catch (error) {
      console.error("Error during submission:", error);
    }
  };

  return (
    <section className="flex w-[100vw] h-[100vh] justify-center items-center">
      <Sidebar />

      <section className="ml-12 px-12 py-6 w-2/3">
        <div className="mb-24">
          <h1 className="font-bold text-8xl text-center">
            Health<span className="text-blue">sync</span>
          </h1>
        </div>

        {/* Form Field */}
        <form
          onSubmit={handleSubmit(onSubmit)}
          className="flex flex-col gap-16"
        >
          <div className="flex flex-col gap-6">
            <div className="flex gap-6 py-3 rounded-2xl">
              <div className="w-1/2 px-4 py-3 bg-white rounded-lg">
                <input
                  {...register("firstName", {
                    required: "First name is required",
                  })}
                  placeholder="First Name"
                  type="text"
                  className="w-full text-lg border-0 outline-none font-light"
                />
              </div>
              <div className="w-1/2 px-4 py-3 bg-white rounded-lg">
                <input
                  {...register("lastName", {
                    required: "Last name is required",
                  })}
                  placeholder="Last Name"
                  type="text"
                  className="w-full text-lg border-0 outline-none font-light"
                />
              </div>
            </div>
            <div className="w-full px-4 py-3 bg-white rounded-lg">
              <input
                {...register("message", {
                  required: "Message is required",
                })}
                placeholder="Enter your message"
                type="text"
                className="w-full text-lg border-0 outline-none font-light"
              />
            </div>
          </div>

          <button
            type="submit"
            className="bg-blue hover:opacity-50 text-md px-2 py-4 font-light text-xl rounded-2xl w-full"
          >
            Submit
          </button>
        </form>
      </section>
    </section>
  );
}

export default FormPage;
