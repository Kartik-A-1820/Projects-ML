from modelrouter.core import featurize,load_rows,MarginalGainRouter,ModelRouter,ModelSpec
def learned_router():return ModelRouter(learned=MarginalGainRouter().fit(load_rows()))
def test_features_fixed_dimension():assert featurize("hello world").shape==(6,)
def test_simple_routes_small_or_medium():assert learned_router().route("rewrite this short email politely").model in {"small","medium"}
def test_hard_query_escalates():assert learned_router().route("debug a race condition across async workers",{"requires_tools":1,"reasoning_steps":5,"coding":1}).model in {"medium","strong"}
def test_cost_constraint_falls_back():assert learned_router().route("design complex distributed architecture",{"reasoning_steps":5},max_cost=1.1).model=="small"
def test_unhealthy_model_not_selected():
 models=[ModelSpec("small",.6,1,100),ModelSpec("medium",.8,2,200),ModelSpec("strong",.95,8,500,healthy=False)];r=ModelRouter(models=models,learned=MarginalGainRouter().fit(load_rows()));assert r.route("debug a race condition",{"reasoning_steps":5,"coding":1}).model!="strong"
