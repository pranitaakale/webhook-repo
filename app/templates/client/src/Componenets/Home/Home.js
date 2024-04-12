import React, {useEffect, useState} from "react";
import {repo_list} from "../../utils/RepoList";
import "./Home.css";

function Home() {
  const [details, setDetails] = useState([]);
  const [displayDetails, setDisplayDetails] = useState([]);
  //   console.log(details.length);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await fetch(
          "http://127.0.0.1:5000/webhook/webhook-data"
        );
        if (!response.ok) {
          throw new Error("Network response was not ok");
        }
        const jsonData = await response.json();
        // console.log(jsonData);
        // jsonData.map((val) => {
        //   //   console.log(val);
        //   if (val.action === "PUSH") {
        //     const push_text =
        //       val.author +
        //       " pushed to " +
        //       val.to_branch +
        //       " on " +
        //       val.timestamp;
        //     const add_push_text = [...displayDetails, push_text];
        //     setDisplayDetails(add_push_text);
        //     // console.log(push_text);
        //   }
        //   if (val.action === "PULL REQUEST") {
        //     const pr_text =
        //       val.author +
        //       " submitted a pull request from " +
        //       val.from_branch +
        //       " to " +
        //       val.to_branch +
        //       " on " +
        //       val.timestamp;
        //     const add_pr_text = [...displayDetails, pr_text];
        // setDisplayDetails(add_pr_text);
        // console.log(pr_text);
        //   }
        // });
        setDetails(jsonData);
      } catch (error) {
        console.log(error.message);
      }
    };

    const intervalId = setInterval(() => {
      fetchData();
    }, 15000);

    return () => clearInterval(intervalId);
  }, []);
  return (
    <div className="home">
      <div className="home_container">
        <div className="home_containerRepo">
          <div className="home_containerRepoTitle">
            <h2>
              Recent Actions on Repository :{" "}
              <a href={repo_list[0].link}>{repo_list[0].name}</a>
            </h2>
          </div>
          <hr />
          <div className="home_containerRepoDetails">
            {details.length > 0 ? (
              <div className="home_containerRepoDetailsList">
                {details.map(
                  (val, index) =>
                    val["action"] === "PUSH" ? (
                      <li key={index}>
                        <span>{val.author}</span>
                        {" pushed to "}
                        <span>{val.to_branch}</span> {" on "}
                        <span>{val.timestamp}</span>
                      </li>
                    ) : (
                      <li key={index}>
                        <span>{val.author}</span>
                        {" submitted a pull request from "}
                        <span>{val.from_branch}</span>
                        {" to "}
                        <span>{val.to_branch}</span>
                        {" on "}
                        <span>{val.timestamp}</span>
                      </li>
                    )
                  // console.log(val, index)
                  //   console.log(val);
                  //   val.action === "PUSH"
                  //     ? console.log(
                  //         val.author,
                  //         " pushed to ",
                  //         val.to_branch,
                  //         " on ",
                  //         val.timestamp
                  //       )
                  //     : console.log(
                  //         val.author,
                  //         "submitted a pull request from ",
                  //         val.from_branch,
                  //         " to ",
                  //         val.to_branch,
                  //         " on ",
                  //         val.timestamp
                  //       );
                )}
              </div>
            ) : (
              <h3>Loading...</h3>
            )}
          </div>
          <div className="home_containerRepoDetails"></div>
        </div>
      </div>
    </div>
  );
}

export default Home;
