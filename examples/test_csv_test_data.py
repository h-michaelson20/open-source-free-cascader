from src.cascade import LLMCascade
import asyncio
import pandas as pd

async def main():
    # Create an instance of LLMCascade
    llm_cascade = LLMCascade()

    # cos_sim = llm_cascade.cosine_similarity_strings("hi i am bob", "hello i am not bob")
    # print(cos_sim)

    # read in the excel spreadsheet
    csv_file_path = './examples/data/science_questions.csv'
    df = pd.read_csv(csv_file_path)

    cos_sims = []
    results = []
    for index in range(0, len(df)):
        question = df.iloc[index, 0]  # Access the first column using iloc
        
        messages = [{
                        "role": "user",
                        "content": f"Answer this in TWO SENTENCES OR LESS: {question}"
                   }]
        vendors = ["sambanova", "googleai", "groq", "groq"]
        models = ["Meta-Llama-3.2-1B-Instruct", "gemini-1.5-flash-8b", "llama3-8b-8192", "llama-3.3-70b-versatile"]
        # CASCADE OF LLAMA 1B, 3B, 8B, 70B
        result, num_models_run = await asyncio.wait_for(llm_cascade.cascade_three_or_more_llm(vendors, models, messages, 0.7), timeout=12)
        # ONLY LLAMA 70B
        #result = await asyncio.wait_for(llm_cascade.get_single_model_result("groq", "llama-3.2-3b-preview", messages), timeout=12)
        await asyncio.sleep(2)
        results.append(result)
        print(f"Index {index} completed.")
        #print(result)

        correct_answer = df.iloc[index, 1]
        llm_answer = results[index]
        cos_sim = llm_cascade.cosine_similarity_strings(correct_answer, llm_answer)
        cos_sims.append(cos_sim)
        print(cos_sim)

    # 18 3B
    # 3 8B
    # OUT OF 46 - so 25 70B

    # NOTE: compare cosine similarities here if didn't wanna do it manually
    print(f"Average cosine similarity: {sum(cos_sims) / len(cos_sims)}")


    # LLAMA 70B INDIVIDUAL RESULTS:
    #[np.float64(0.07332355751067667), np.float64(0.5006010821645457), np.float64(0.4082482904638631), np.float64(0.6781458226345989), np.float64(0.38664114563451135), np.float64(0.4583492485141055), np.float64(0.209980262782904), np.float64(0.4271210980886246), np.float64(0.35445877847928325), np.float64(0.5580523396538208), np.float64(0.5167050676973537), np.float64(0.2898754521821014), np.float64(0.5874269508076823), np.float64(0.23939494881986928), np.float64(0.3202223803567701), np.float64(0.27472112789737807), np.float64(0.5704356452719495), np.float64(0.5676987574362224), np.float64(0.5131255911961764), np.float64(0.39348799079590163), np.float64(0.5004732608726313), np.float64(0.5895013277353356), np.float64(0.58554004376912), np.float64(0.606119015745411), np.float64(0.6386780131801737), np.float64(0.3194292535910661), np.float64(0.5265602957000086), np.float64(0.30905754998184354), np.float64(0.4485426135725302), np.float64(0.4880935300919763), np.float64(0.5691245004265075), np.float64(0.0), np.float64(0.24641644145347896), np.float64(0.41963979908441684), np.float64(0.3265986323710903), np.float64(0.21469688008935395), np.float64(0.5643322103800708), np.float64(0.5017452060042545), np.float64(0.7351532181632235), np.float64(0.5640760748177662), np.float64(0.6400757530925303), np.float64(0.659231724180059), np.float64(0.26539552107881487), np.float64(0.49239912322395957), np.float64(0.5968491905238342), np.float64(0.2831827358942995), np.float64(0.36025803716501004), np.float64(0.2419553954370992), np.float64(0.5094445355028789), np.float64(0.27524094128159016)]
    # Average cosine similarity: 0.4361165272559736

    # LLAMA CASCADE INDIVIDUAL RESULTS:
    # 0, 0.5075459213253762,0.21281413268968719,0.5628780357842335,0.31984651050360063,0.4375875262587531,0.2817180849095055,0.31492602902248096,0.08581943515359347,0.4275930552470683,0.5329405848726388,0.28067069969390585,0.5499719409228703,0.3079201435678004,0.3018927632559766,0.21428571428571427,0.584126912832442,0.30071150760970466,0.46739672050221975,0.3077192441364928,0.487869376909045,0.5360201681382464,0.5730698830937557,0.5443474098074709,0.6659027536546027,0.48340047695154065,0.7171087882915774,0.36757352205735255,0.5499266813300749,0.08512565307587484,0.22555354977384037,0.6609713434659001,0.3312945782245396,0.5066403971048988,0.6659733054112931,0.4767312946227962,0.7037037037037037,0.554265307725427,0.7692772189617514,0.661925769268946,0.3649794388034841,0.5223945248602444,0.5855400437691198,0.2831827358942995,0.35946277018081774,0.3585685828003181,0.3465719328378872,0.18973665961010275

        # vendors = ["sambanova", "openrouter", "groq", "groq"]
        # models = ["Meta-Llama-3.2-1B-Instruct", "meta-llama/llama-3.2-3b-instruct:free", "llama3-8b-8192", "llama-3.3-70b-versatile"]
        # output, num_models_run = await llm_cascade.cascade_three_or_more_llm_basic(vendors, models, messages, 0.7)


    # this is the cascading two llms basic idea
    # messages=[{
    #             "role": "user",
    #             "content": "Who is yash agrawal?"
    #         }]
    # vendors = ["sambanova", "openrouter", "groq", "groq"]
    # models = ["Meta-Llama-3.2-1B-Instruct", "meta-llama/llama-3.2-3b-instruct:free", "llama3-8b-8192", "llama-3.3-70b-versatile"]
    # output, num_models_run = await llm_cascade.cascade_three_or_more_llm_basic(vendors, models, messages, 0.7)
    # print(40*"-")
    # print(f"Final result: {output}")
    # print(f"Models run up to: {models[num_models_run-1]}")

if __name__ == "__main__":
    asyncio.run(main())