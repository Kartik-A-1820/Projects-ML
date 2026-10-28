# Portfolio source inventory — 27 October 2026

Observed source snapshot before this maintenance change: `115527ec75036707ae672d969aa58295e76fb691`.
This document verifies repository file presence, not execution of every lab.

| Series | Present week folders | Missing through latest present week |
| --- | --- | --- |
| Tuesday engineering | 01–31, 33 (requirements-only scaffold), 37 | 32, 34–36 |
| Saturday data science | 01–05, 07 | 06 |

## Maintenance verification

DS Week 05 was missing README, implementation, dependencies, and notebook. A
runnable reconstruction now supplies these plus architecture notes. Its original
two metric tests and three pipeline tests pass, and a new synthetic smoke report
was executed. Historical `artifacts/metrics.json` remains unchanged and is not
claimed as reproduced. MovieLens evaluation has not run.

The root audit utility has a passing fixture-based regression test. It checks
presence only; `runtime_verified` is always false in its inventory output.
Other projects' historical verification, Drive, and Library badges were not
revalidated by this maintenance pass.

## Migration identity conflicts

- Week 33 is named **MCPGuard Control Plane** in the migration ledger, while the
  Week 37 series registry calls it **streaming voice edge**. The current tree
  contains `weekly-projects/week-33-streamvoice-edge/requirements.txt` only.
  The folder identifies a StreamVoice scaffold but has no implementation or
  README. Resolve the historical MCPGuard proposal against original artifacts
  before treating Week 33 as a complete migrated project.
- Weeks 32 and 34 are pending in the migration ledger and absent here.
- Weeks 35 (SpecPilot) and 36 (EraseProof) are described as local artifacts in
  the Week 37 registry but their source folders are absent here.
- DS Week 06 is named in the DS registry but its source folder is absent.
- These are repository coverage gaps, not proof that the work does not exist
  in another location. Do not generate duplicate weeks merely to fill them.

## Present source folders

### Tuesday engineering

- [week-01-localdoc-rag](weekly-projects/week-01-localdoc-rag/)
- [week-02-smartresume-nlp](weekly-projects/week-02-smartresume-nlp/)
- [week-03-visiontrack-ai](weekly-projects/week-03-visiontrack-ai/)
- [week-04-transformersentiment-lab](weekly-projects/week-04-transformersentiment-lab/)
- [week-05-semanticsearch-engine](weekly-projects/week-05-semanticsearch-engine/)
- [week-06-ocrdoc-intelligence](weekly-projects/week-06-ocrdoc-intelligence/)
- [week-07-lora-finetune-lab](weekly-projects/week-07-lora-finetune-lab/)
- [week-08-multipdf-rag](weekly-projects/week-08-multipdf-rag/)
- [week-09-visionsearch-clip](weekly-projects/week-09-visionsearch-clip/)
- [week-10-agenticrag-local](weekly-projects/week-10-agenticrag-local/)
- [week-11-nlpintent-engine](weekly-projects/week-11-nlpintent-engine/)
- [week-12-modelexplain-ml](weekly-projects/week-12-modelexplain-ml/)
- [week-13-videorag-local](weekly-projects/week-13-videorag-local/)
- [week-14-codepilot-mini](weekly-projects/week-14-codepilot-mini/)
- [week-15-federatedllm-lite](weekly-projects/week-15-federatedllm-lite/)
- [week-16-graphrag-enterprise](weekly-projects/week-16-graphrag-enterprise/)
- [week-17-visionagent-studio](weekly-projects/week-17-visionagent-studio/)
- [week-18-ragguard-local](weekly-projects/week-18-ragguard-local/)
- [week-19-datasynth-llm](weekly-projects/week-19-datasynth-llm/)
- [week-20-modelrouter-local](weekly-projects/week-20-modelrouter-local/)
- [week-21-hybridsearch-rag](weekly-projects/week-21-hybridsearch-rag/)
- [week-22-llmcache-engine](weekly-projects/week-22-llmcache-engine/)
- [week-23-autolabel-nlp](weekly-projects/week-23-autolabel-nlp/)
- [week-24-tinyllm-finetuner](weekly-projects/week-24-tinyllm-finetuner/)
- [week-25-multiagent-researcher](weekly-projects/week-25-multiagent-researcher/)
- [week-26-visionrag-local](weekly-projects/week-26-visionrag-local/)
- [week-27-mlops-modelregistry](weekly-projects/week-27-mlops-modelregistry/)
- [week-28-edgevision-analytics](weekly-projects/week-28-edgevision-analytics/)
- [week-29-driftwatch-ml](weekly-projects/week-29-driftwatch-ml/)
- [week-30-promptshield-local](weekly-projects/week-30-promptshield-local/)
- [week-31-continuallearn-nlp](weekly-projects/week-31-continuallearn-nlp/)
- [week-33-streamvoice-edge](weekly-projects/week-33-streamvoice-edge/)
- [week-37-contracttrace-agent-transactions](weekly-projects/week-37-contracttrace-agent-transactions/)

### Saturday data science

- [ds-week-01-calibrated-credit-risk](data-science-labs/ds-week-01-calibrated-credit-risk/)
- [ds-week-02-uncertainty-aware-turbofan-rul](data-science-labs/ds-week-02-uncertainty-aware-turbofan-rul/)
- [ds-week-03-causal-uplift-targeting](data-science-labs/ds-week-03-causal-uplift-targeting/)
- [ds-week-04-censor-aware-telco-survival](data-science-labs/ds-week-04-censor-aware-telco-survival/)
- [ds-week-05-longtail-sequential-recommendation](data-science-labs/ds-week-05-longtail-sequential-recommendation/)
- [ds-week-07-phishing-domain-generalization](data-science-labs/ds-week-07-phishing-domain-generalization/)
