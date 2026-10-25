> Historical diagnostic snapshot: the later unstructured investigation repaired evidence_48 parsing, reducing current full-run warnings to 343. See unstructured_report.md and coverage_report.md for the current output; older counts/digests below describe the earlier run.

# System activity mapping investigation

All 4011 activity rows were indexed. 12 rows contain a complete identifier matching the supplied identity/alias index. There are 12 LINK_RESOURCE_IDENTITY events.

All 518/518 request emails resolve to one subject when eligible current/historical identity data are considered. The coverage gap is primarily resource ownership/state, not failure to identify the person.

Compared with the prior details scanner across the actual audit cutoffs, the new mapper yields **0 additional ownership bindings** on the supplied dataset. Existing direct identity-bearing activity rows were already indexed by the old resolver.

| Event type | Rows |
| --- | --- |
| ANONYMIZE_RECORD | 204 |
| BLOCK_RESTORE | 36 |
| CHECK_DATA_FLOW | 89 |
| CHECK_RESTORE_ACCESS | 28 |
| CLASSIFY_REQUEST | 10 |
| CREATE_EXPORT | 155 |
| DELETE_RECORD | 890 |
| DISABLE_DATA_FLOW | 36 |
| INDEX_RECORD | 400 |
| LINK_RESOURCE_IDENTITY | 12 |
| REDACT_RECORD | 173 |
| REFRESH_CACHE | 284 |
| RESTORE_BACKUP | 1 |
| RETAIN_RECORD | 206 |
| SEND_EMAIL | 368 |
| SYNC_RECORD | 447 |
| UPDATE_RECORD | 672 |

## What the new mapper provides

- Exact, case-insensitive complete email/user/hash tokens and normalized international phone numbers; user_05 does not match user_050.
- UTC-aware inclusive event_time cutoff, sorted chronologically using parsed timestamps; malformed times fail explicitly.
- Identity matches carry matched identifiers and activity IDs. Anonymous later/earlier history is followed only for the explicitly linked resource, within the cutoff.
- Conflicting subject links stay conflicting, with full activity provenance; no owner is selected arbitrarily.
- DELETE/ANONYMIZE/REDACT/SYNC results remain workflow claims. Summaries return status UNKNOWN, verified false and empty state evidence_id; claimed_state and claimed_activity_id are diagnostic fields only.
- ANONYMIZE_RECORD correctly maps to the reported ANONYMIZED claim. It is not silently mislabeled REDACTED.

## Identity-bearing activity rows

| Activity | Resource | Matched subjects |
| --- | --- | --- |
| activity_4000 | account_5762 | user_11 |
| activity_4001 | search_428 | user_13 |
| activity_4002 | data_flow_1121 | user_14 |
| activity_4003 | analytics_7438 | user_20 |
| activity_4004 | export_1260 | user_18 |
| activity_4005 | support_1034 | user_22 |
| activity_4006 | backup_9287 | user_16 |
| activity_4007 | object_19 | user_07 |
| activity_4008 | marketing_001 | user_09 |
| activity_4009 | export_1842 | user_18 |
| activity_4010 | audit_record_003 | user_03 |
| activity_4011 | tombstone_17 | user_17 |

## Cases with missing primary-state coverage

Identity seed rows are eligible rows explicitly mentioning a known identifier. History rows include only the same resource IDs, not nearby unrelated events. Finding a resource/history does not prove its current state.

| Case | Identity seed rows | Related history rows | Linked resources | Explicit primary seed rows |
| --- | --- | --- | --- | --- |
| case_33 | 2 | 2 | export_1260, export_1842 | 0 |
| case_35 | 1 | 2 | search_428 | 0 |
| case_39 | 1 | 1 | data_flow_1121 | 0 |
| case_45 | 1 | 1 | audit_record_003 | 0 |
| case_47 | 0 | 0 | none | 0 |
| case_48 | 0 | 0 | none | 0 |
| case_49 | 0 | 0 | none | 0 |
| case_50 | 1 | 1 | analytics_7438 | 0 |
| case_52 | 1 | 1 | export_1260 | 0 |
| case_53 | 1 | 1 | support_1034 | 0 |
| case_54 | 0 | 0 | none | 0 |
| case_55 | 1 | 1 | backup_9287 | 0 |
| case_56 | 0 | 0 | none | 0 |
| case_57 | 0 | 0 | none | 0 |
| case_58 | 0 | 0 | none | 0 |
| case_59 | 0 | 0 | none | 0 |
| case_60 | 0 | 0 | none | 0 |
| case_61 | 1 | 1 | object_19 | 0 |
| case_62 | 0 | 0 | none | 0 |
| case_63 | 1 | 1 | marketing_001 | 0 |
| case_64 | 0 | 0 | none | 0 |
| case_65 | 0 | 0 | none | 0 |
| case_66 | 0 | 0 | none | 0 |
| case_68 | 0 | 0 | none | 0 |
| case_69 | 0 | 0 | none | 0 |
| case_70 | 0 | 0 | none | 0 |
| case_71 | 0 | 0 | none | 0 |
| case_72 | 0 | 0 | none | 0 |
| case_74 | 0 | 0 | none | 0 |
| case_75 | 0 | 0 | none | 0 |
| case_76 | 0 | 0 | none | 0 |
| case_78 | 0 | 0 | none | 0 |
| case_94 | 0 | 0 | none | 0 |
| case_95 | 0 | 0 | none | 0 |
| case_96 | 0 | 0 | none | 0 |
| case_97 | 0 | 0 | none | 0 |
| case_98 | 0 | 0 | none | 0 |
| case_99 | 0 | 0 | none | 0 |
| case_100 | 0 | 0 | none | 0 |
| case_101 | 0 | 0 | none | 0 |
| case_102 | 0 | 0 | none | 0 |
| case_103 | 0 | 0 | none | 0 |
| case_104 | 0 | 0 | none | 0 |
| case_106 | 0 | 0 | none | 0 |
| case_107 | 0 | 0 | none | 0 |
| case_108 | 0 | 0 | none | 0 |
| case_109 | 0 | 0 | none | 0 |
| case_110 | 0 | 0 | none | 0 |
| case_111 | 0 | 0 | none | 0 |
| case_112 | 0 | 0 | none | 0 |
| case_114 | 0 | 0 | none | 0 |
| case_116 | 0 | 0 | none | 0 |
| case_118 | 0 | 0 | none | 0 |
| case_119 | 0 | 0 | none | 0 |
| case_120 | 0 | 0 | none | 0 |
| case_122 | 0 | 0 | none | 0 |
| case_123 | 0 | 0 | none | 0 |
| case_124 | 0 | 0 | none | 0 |
| case_125 | 0 | 0 | none | 0 |
| case_126 | 0 | 0 | none | 0 |
| case_127 | 0 | 0 | none | 0 |
| case_128 | 0 | 0 | none | 0 |
| case_130 | 0 | 0 | none | 0 |
| case_131 | 0 | 0 | none | 0 |
| case_132 | 0 | 0 | none | 0 |
| case_143 | 0 | 0 | none | 0 |
| case_144 | 0 | 0 | none | 0 |
| case_145 | 0 | 0 | none | 0 |
| case_146 | 0 | 0 | none | 0 |
| case_147 | 0 | 0 | none | 0 |
| case_148 | 0 | 0 | none | 0 |
| case_149 | 0 | 0 | none | 0 |
| case_150 | 0 | 0 | none | 0 |
| case_151 | 0 | 0 | none | 0 |
| case_152 | 0 | 0 | none | 0 |
| case_154 | 0 | 0 | none | 0 |
| case_155 | 0 | 0 | none | 0 |
| case_156 | 0 | 0 | none | 0 |
| case_157 | 0 | 0 | none | 0 |
| case_158 | 0 | 0 | none | 0 |
| case_159 | 0 | 0 | none | 0 |
| case_160 | 0 | 0 | none | 0 |
| case_161 | 0 | 0 | none | 0 |
| case_162 | 0 | 0 | none | 0 |
| case_166 | 0 | 0 | none | 0 |
| case_168 | 0 | 0 | none | 0 |
| case_169 | 0 | 0 | none | 0 |
| case_171 | 0 | 0 | none | 0 |
| case_172 | 0 | 0 | none | 0 |
| case_173 | 0 | 0 | none | 0 |
| case_174 | 0 | 0 | none | 0 |
| case_175 | 0 | 0 | none | 0 |
| case_176 | 0 | 0 | none | 0 |
| case_178 | 0 | 0 | none | 0 |
| case_179 | 0 | 0 | none | 0 |
| case_180 | 0 | 0 | none | 0 |
| case_181 | 0 | 0 | none | 0 |
| case_182 | 0 | 0 | none | 0 |
| case_183 | 0 | 0 | none | 0 |
| case_184 | 0 | 0 | none | 0 |
| case_185 | 0 | 0 | none | 0 |
| case_186 | 0 | 0 | none | 0 |
| case_188 | 0 | 0 | none | 0 |
| case_190 | 0 | 0 | none | 0 |
| case_191 | 0 | 0 | none | 0 |
| case_192 | 0 | 0 | none | 0 |
| case_194 | 0 | 0 | none | 0 |
| case_197 | 0 | 0 | none | 0 |
| case_198 | 0 | 0 | none | 0 |
| case_200 | 0 | 0 | none | 0 |
| case_203 | 0 | 0 | none | 0 |
| case_204 | 0 | 0 | none | 0 |
| case_205 | 0 | 0 | none | 0 |
| case_206 | 0 | 0 | none | 0 |
| case_207 | 0 | 0 | none | 0 |
| case_208 | 0 | 0 | none | 0 |
| case_209 | 0 | 0 | none | 0 |
| case_210 | 0 | 0 | none | 0 |
| case_212 | 0 | 0 | none | 0 |
| case_213 | 0 | 0 | none | 0 |
| case_214 | 0 | 0 | none | 0 |
| case_215 | 0 | 0 | none | 0 |
| case_216 | 0 | 0 | none | 0 |
| case_217 | 0 | 0 | none | 0 |
| case_218 | 0 | 0 | none | 0 |
| case_219 | 0 | 0 | none | 0 |
| case_220 | 0 | 0 | none | 0 |
| case_221 | 0 | 0 | none | 0 |
| case_222 | 0 | 0 | none | 0 |
| case_224 | 0 | 0 | none | 0 |
| case_225 | 0 | 0 | none | 0 |
| case_226 | 0 | 0 | none | 0 |
| case_227 | 0 | 0 | none | 0 |
| case_228 | 0 | 0 | none | 0 |
| case_229 | 0 | 0 | none | 0 |
| case_230 | 0 | 0 | none | 0 |
| case_231 | 0 | 0 | none | 0 |
| case_232 | 0 | 0 | none | 0 |
| case_234 | 0 | 0 | none | 0 |
| case_236 | 0 | 0 | none | 0 |
| case_240 | 0 | 0 | none | 0 |
| case_241 | 0 | 0 | none | 0 |
| case_242 | 0 | 0 | none | 0 |
| case_243 | 0 | 0 | none | 0 |
| case_244 | 0 | 0 | none | 0 |
| case_245 | 0 | 0 | none | 0 |
| case_246 | 0 | 0 | none | 0 |
| case_248 | 0 | 0 | none | 0 |
| case_250 | 0 | 0 | none | 0 |
| case_251 | 0 | 0 | none | 0 |
| case_252 | 0 | 0 | none | 0 |
| case_253 | 0 | 0 | none | 0 |
| case_254 | 0 | 0 | none | 0 |
| case_255 | 0 | 0 | none | 0 |
| case_256 | 0 | 0 | none | 0 |
| case_257 | 0 | 0 | none | 0 |
| case_258 | 0 | 0 | none | 0 |
| case_260 | 0 | 0 | none | 0 |
| case_262 | 0 | 0 | none | 0 |
| case_274 | 0 | 0 | none | 0 |
| case_275 | 0 | 0 | none | 0 |
| case_276 | 0 | 0 | none | 0 |
| case_277 | 0 | 0 | none | 0 |
| case_278 | 0 | 0 | none | 0 |
| case_279 | 0 | 0 | none | 0 |
| case_280 | 0 | 0 | none | 0 |
| case_281 | 0 | 0 | none | 0 |
| case_282 | 0 | 0 | none | 0 |
| case_284 | 0 | 0 | none | 0 |
| case_287 | 0 | 0 | none | 0 |
| case_288 | 0 | 0 | none | 0 |
| case_289 | 0 | 0 | none | 0 |
| case_290 | 0 | 0 | none | 0 |
| case_291 | 0 | 0 | none | 0 |
| case_293 | 0 | 0 | none | 0 |
| case_294 | 0 | 0 | none | 0 |
| case_295 | 0 | 0 | none | 0 |
| case_296 | 0 | 0 | none | 0 |
| case_297 | 0 | 0 | none | 0 |
| case_298 | 0 | 0 | none | 0 |
| case_299 | 0 | 0 | none | 0 |
| case_300 | 0 | 0 | none | 0 |
| case_301 | 0 | 0 | none | 0 |
| case_302 | 0 | 0 | none | 0 |
| case_303 | 0 | 0 | none | 0 |
| case_304 | 0 | 0 | none | 0 |
| case_305 | 0 | 0 | none | 0 |
| case_306 | 0 | 0 | none | 0 |
| case_308 | 0 | 0 | none | 0 |
| case_309 | 0 | 0 | none | 0 |
| case_310 | 0 | 0 | none | 0 |
| case_311 | 0 | 0 | none | 0 |
| case_312 | 0 | 0 | none | 0 |
| case_313 | 0 | 0 | none | 0 |
| case_314 | 0 | 0 | none | 0 |
| case_315 | 0 | 0 | none | 0 |
| case_316 | 0 | 0 | none | 0 |
| case_317 | 0 | 0 | none | 0 |
| case_318 | 0 | 0 | none | 0 |
| case_319 | 0 | 0 | none | 0 |
| case_320 | 0 | 0 | none | 0 |
| case_321 | 0 | 0 | none | 0 |
| case_322 | 0 | 0 | none | 0 |
| case_325 | 0 | 0 | none | 0 |
| case_328 | 0 | 0 | none | 0 |
| case_329 | 0 | 0 | none | 0 |
| case_330 | 0 | 0 | none | 0 |
| case_332 | 0 | 0 | none | 0 |
| case_334 | 0 | 0 | none | 0 |
| case_335 | 0 | 0 | none | 0 |
| case_336 | 0 | 0 | none | 0 |
| case_337 | 0 | 0 | none | 0 |
| case_338 | 0 | 0 | none | 0 |
| case_339 | 0 | 0 | none | 0 |
| case_340 | 0 | 0 | none | 0 |
| case_341 | 0 | 0 | none | 0 |
| case_342 | 0 | 0 | none | 0 |
| case_343 | 0 | 0 | none | 0 |
| case_344 | 0 | 0 | none | 0 |
| case_345 | 0 | 0 | none | 0 |
| case_346 | 0 | 0 | none | 0 |
| case_347 | 0 | 0 | none | 0 |
| case_348 | 0 | 0 | none | 0 |
| case_349 | 0 | 0 | none | 0 |
| case_350 | 0 | 0 | none | 0 |
| case_351 | 0 | 0 | none | 0 |
| case_352 | 0 | 0 | none | 0 |
| case_353 | 0 | 0 | none | 0 |
| case_354 | 0 | 0 | none | 0 |
| case_356 | 0 | 0 | none | 0 |
| case_358 | 0 | 0 | none | 0 |
| case_359 | 0 | 0 | none | 0 |
| case_360 | 0 | 0 | none | 0 |
| case_361 | 0 | 0 | none | 0 |
| case_362 | 0 | 0 | none | 0 |
| case_373 | 0 | 0 | none | 0 |
| case_376 | 0 | 0 | none | 0 |
| case_377 | 0 | 0 | none | 0 |
| case_382 | 0 | 0 | none | 0 |
| case_393 | 0 | 0 | none | 0 |
| case_394 | 0 | 0 | none | 0 |
| case_395 | 0 | 0 | none | 0 |
| case_396 | 0 | 0 | none | 0 |
| case_397 | 0 | 0 | none | 0 |
| case_398 | 0 | 0 | none | 0 |
| case_399 | 0 | 0 | none | 0 |
| case_400 | 0 | 0 | none | 0 |
| case_401 | 0 | 0 | none | 0 |
| case_402 | 0 | 0 | none | 0 |
| case_403 | 0 | 0 | none | 0 |
| case_404 | 0 | 0 | none | 0 |
| case_406 | 0 | 0 | none | 0 |
| case_407 | 0 | 0 | none | 0 |
| case_408 | 0 | 0 | none | 0 |
| case_409 | 0 | 0 | none | 0 |
| case_410 | 0 | 0 | none | 0 |
| case_411 | 0 | 0 | none | 0 |
| case_412 | 0 | 0 | none | 0 |
| case_423 | 0 | 0 | none | 0 |
| case_424 | 0 | 0 | none | 0 |
| case_425 | 0 | 0 | none | 0 |
| case_426 | 0 | 0 | none | 0 |
| case_427 | 0 | 0 | none | 0 |
| case_428 | 0 | 0 | none | 0 |
| case_430 | 0 | 0 | none | 0 |
| case_431 | 0 | 0 | none | 0 |
| case_432 | 0 | 0 | none | 0 |
| case_443 | 0 | 0 | none | 0 |
| case_444 | 0 | 0 | none | 0 |
| case_445 | 0 | 0 | none | 0 |
| case_446 | 0 | 0 | none | 0 |
| case_447 | 0 | 0 | none | 0 |
| case_448 | 0 | 0 | none | 0 |
| case_449 | 0 | 0 | none | 0 |
| case_450 | 0 | 0 | none | 0 |
| case_451 | 0 | 0 | none | 0 |
| case_452 | 0 | 0 | none | 0 |
| case_454 | 0 | 0 | none | 0 |
| case_455 | 0 | 0 | none | 0 |
| case_456 | 0 | 0 | none | 0 |
| case_457 | 0 | 0 | none | 0 |
| case_458 | 0 | 0 | none | 0 |
| case_459 | 0 | 0 | none | 0 |
| case_460 | 0 | 0 | none | 0 |
| case_461 | 0 | 0 | none | 0 |
| case_462 | 0 | 0 | none | 0 |
| case_463 | 0 | 0 | none | 0 |
| case_464 | 0 | 0 | none | 0 |
| case_466 | 0 | 0 | none | 0 |
| case_467 | 0 | 0 | none | 0 |
| case_468 | 0 | 0 | none | 0 |
| case_469 | 0 | 0 | none | 0 |
| case_470 | 0 | 0 | none | 0 |
| case_471 | 0 | 0 | none | 0 |
| case_472 | 0 | 0 | none | 0 |
| case_473 | 0 | 0 | none | 0 |
| case_474 | 0 | 0 | none | 0 |
| case_476 | 0 | 0 | none | 0 |
| case_478 | 0 | 0 | none | 0 |
| case_479 | 0 | 0 | none | 0 |
| case_480 | 0 | 0 | none | 0 |
| case_481 | 0 | 0 | none | 0 |
| case_482 | 0 | 0 | none | 0 |
| case_483 | 0 | 0 | none | 0 |
| case_484 | 0 | 0 | none | 0 |
| case_485 | 0 | 0 | none | 0 |
| case_488 | 0 | 0 | none | 0 |
| case_490 | 0 | 0 | none | 0 |
| case_492 | 0 | 0 | none | 0 |
| case_493 | 0 | 0 | none | 0 |
| case_494 | 0 | 0 | none | 0 |
| case_495 | 0 | 0 | none | 0 |
| case_496 | 0 | 0 | none | 0 |
| case_497 | 0 | 0 | none | 0 |
| case_498 | 0 | 0 | none | 0 |
| case_500 | 0 | 0 | none | 0 |
| case_502 | 0 | 0 | none | 0 |
| case_503 | 0 | 0 | none | 0 |
| case_504 | 0 | 0 | none | 0 |
| case_505 | 0 | 0 | none | 0 |
| case_506 | 0 | 0 | none | 0 |
| case_507 | 0 | 0 | none | 0 |
| case_508 | 0 | 0 | none | 0 |
| case_509 | 0 | 0 | none | 0 |
| case_510 | 0 | 0 | none | 0 |
| case_512 | 0 | 0 | none | 0 |
| case_513 | 0 | 0 | none | 0 |
| case_514 | 0 | 0 | none | 0 |
| case_515 | 0 | 0 | none | 0 |
| case_516 | 0 | 0 | none | 0 |
| case_517 | 0 | 0 | none | 0 |
| case_518 | 0 | 0 | none | 0 |
| case_519 | 0 | 0 | none | 0 |
| case_520 | 0 | 0 | none | 0 |
| case_521 | 0 | 0 | none | 0 |
| case_522 | 0 | 0 | none | 0 |
| case_524 | 0 | 0 | none | 0 |
| case_526 | 0 | 0 | none | 0 |
| case_527 | 0 | 0 | none | 0 |
| case_528 | 0 | 0 | none | 0 |
| case_529 | 0 | 0 | none | 0 |
| case_530 | 0 | 0 | none | 0 |
| case_531 | 0 | 0 | none | 0 |
| case_532 | 0 | 0 | none | 0 |
| case_543 | 0 | 0 | none | 0 |
| case_544 | 0 | 0 | none | 0 |
| case_545 | 0 | 0 | none | 0 |
| case_546 | 0 | 0 | none | 0 |
| case_547 | 0 | 0 | none | 0 |
| case_548 | 0 | 0 | none | 0 |
| case_549 | 0 | 0 | none | 0 |
| case_550 | 0 | 0 | none | 0 |

## Measured validation

- 23/23 synthetic regression tests passed, including five activity-specific tests.
- Public sample performance remains 23/32 status matches and 9/32 exact rows.
- Full output has 518 rows and 353 coverage-warning cases. Its digest is `510515ddebeb60b4086656da21fc9bf07c99380d33c264f86ef0ed4b3bdf03c7`.
- No later evidence, fabricated resource IDs, activity adjacency or reported-success claims were used to reduce the warning count.
