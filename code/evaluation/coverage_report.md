# Full-run evidence coverage

Processed 518 requests. **343 cases** have unresolved evidence coverage. These are best-effort predictions, not a complete evidence-backed submission.

## Measured root-cause groups

| Primary reason per affected case | Cases |
| --- | --- |
| Required state field not visible in the supplied evidence | 1 |
| No explicit primary ownership link found by implemented extractors | 262 |
| Explicit primary identity link found only in later evidence; excluded from predictions | 80 |

There may be several issues per case. The grouping above counts each affected case once. Detailed issue totals:

- 342: `No identity-linked primary account state`
- 1: `backup_9287: missing state fields`
- 1: `tombstone_17: missing state fields`

## What was checked and changed

- Identity history has 306 rows with fields `{'phone': 92, 'email': 107, 'email_hash': 107}`. Both old and new values from eligible rows are indexed; the problem is not simply that old emails were skipped.
- Current-email SHA-256 derivation was checked against all 850 supplied identities: verified. Only eligible email aliases are hashed.
- Telephone aliases now use the same supplied international digits despite punctuation differences. No fuzzy name/phone matching or guessed country codes are used.
- Explicit source/parent resource references are resolved in both directions through complete connected components, including chains longer than three links. IDs mentioned only in prose are not ownership edges.
- A linked resource without a row can be checked against a declared collection snapshot, but a successful deletion activity is still not accepted as state proof. System routing and state evidence remain separate.
- All manifest source files were opened: `{'.log': 26, '.json': 28, '.txt': 1, '.png': 11, '.sql': 24, '.pdf': 4}`. PDF text and reviewed image fields participate in retrieval. The two image-state gaps remain unresolved because unseen fields cannot be inferred from a console title or health indicator.
- File availability and internal observation/scope times are checked against the cutoff. The latest observation is chosen per linked resource; equal-time replica violations take precedence over an absent primary.
- Reading a later capture for this diagnostic does not authorize using it to reconstruct an earlier audit. No later links in the table below are fed into the prediction engine.

## Per-case triage

| Case | Subject | Reason | Eligible historical values | Eligible unattributed primary resources | Sources linked to subject |
| --- | --- | --- | --- | --- | --- |
| case_33 | user_18 | PRIMARY_LINK_ONLY_AFTER_CUTOFF | 0 | 17 | evidence_18, evidence_23 |
| case_35 | user_13 | PRIMARY_LINK_ONLY_AFTER_CUTOFF | 0 | 21 | evidence_09 |
| case_39 | user_14 | PRIMARY_LINK_ONLY_AFTER_CUTOFF | 0 | 20 | evidence_14 |
| case_45 | user_03 | NO_PRIMARY_LINK_FOUND | 0 | 24 | evidence_37, evidence_55 |
| case_46 | user_17 | MISSING_VISIBLE_FIELDS | 0 | 3 | evidence_42, evidence_67 |
| case_47 | user_45 | NO_PRIMARY_LINK_FOUND | 4 | 27 | evidence_94 |
| case_48 | user_46 | NO_PRIMARY_LINK_FOUND | 4 | 27 | evidence_94 |
| case_49 | user_47 | NO_PRIMARY_LINK_FOUND | 4 | 27 | evidence_94 |
| case_50 | user_20 | PRIMARY_LINK_ONLY_AFTER_CUTOFF | 2 | 14 | evidence_19 |
| case_52 | user_18 | PRIMARY_LINK_ONLY_AFTER_CUTOFF | 0 | 12 | evidence_23 |
| case_53 | user_22 | NO_PRIMARY_LINK_FOUND | 0 | 9 | evidence_28 |
| case_54 | user_52 | NO_PRIMARY_LINK_FOUND | 0 | 27 | evidence_05 |
| case_55 | user_16 | PRIMARY_LINK_ONLY_AFTER_CUTOFF | 0 | 9 | evidence_32 |
| case_56 | user_54 | NO_PRIMARY_LINK_FOUND | 4 | 27 | evidence_05 |
| case_57 | user_55 | NO_PRIMARY_LINK_FOUND | 2 | 27 | evidence_05 |
| case_58 | user_56 | NO_PRIMARY_LINK_FOUND | 0 | 27 | evidence_05 |
| case_59 | user_57 | NO_PRIMARY_LINK_FOUND | 0 | 27 | evidence_05 |
| case_60 | user_58 | NO_PRIMARY_LINK_FOUND | 0 | 27 | evidence_05 |
| case_61 | user_07 | NO_PRIMARY_LINK_FOUND | 0 | 3 | evidence_46 |
| case_62 | user_60 | NO_PRIMARY_LINK_FOUND | 4 | 27 | evidence_05 |
| case_63 | user_09 | NO_PRIMARY_LINK_FOUND | 0 | 29 | evidence_60 |
| case_64 | user_62 | PRIMARY_LINK_ONLY_AFTER_CUTOFF | 0 | 29 | evidence_93 |
| case_65 | user_63 | PRIMARY_LINK_ONLY_AFTER_CUTOFF | 0 | 29 | evidence_93 |
| case_66 | user_64 | PRIMARY_LINK_ONLY_AFTER_CUTOFF | 4 | 29 | evidence_93 |
| case_68 | user_66 | PRIMARY_LINK_ONLY_AFTER_CUTOFF | 0 | 29 | evidence_93 |
| case_69 | user_67 | PRIMARY_LINK_ONLY_AFTER_CUTOFF | 0 | 29 | evidence_93 |
| case_70 | user_68 | PRIMARY_LINK_ONLY_AFTER_CUTOFF | 0 | 29 | evidence_93 |
| case_71 | user_69 | PRIMARY_LINK_ONLY_AFTER_CUTOFF | 0 | 29 | evidence_93 |
| case_72 | user_70 | PRIMARY_LINK_ONLY_AFTER_CUTOFF | 2 | 29 | evidence_93 |
| case_74 | user_72 | NO_PRIMARY_LINK_FOUND | 0 | 24 | evidence_91 |
| case_75 | user_73 | NO_PRIMARY_LINK_FOUND | 0 | 24 | evidence_91 |
| case_76 | user_74 | NO_PRIMARY_LINK_FOUND | 0 | 24 | evidence_91 |
| case_78 | user_76 | NO_PRIMARY_LINK_FOUND | 0 | 24 | evidence_91 |
| case_94 | user_92 | NO_PRIMARY_LINK_FOUND | 4 | 21 | evidence_89 |
| case_95 | user_93 | NO_PRIMARY_LINK_FOUND | 0 | 21 | evidence_89 |
| case_96 | user_94 | NO_PRIMARY_LINK_FOUND | 0 | 21 | evidence_89 |
| case_97 | user_95 | NO_PRIMARY_LINK_FOUND | 4 | 21 | evidence_89 |
| case_98 | user_96 | NO_PRIMARY_LINK_FOUND | 4 | 21 | evidence_89 |
| case_99 | user_97 | NO_PRIMARY_LINK_FOUND | 0 | 21 | evidence_89 |
| case_100 | user_98 | NO_PRIMARY_LINK_FOUND | 4 | 21 | evidence_89 |
| case_101 | user_99 | NO_PRIMARY_LINK_FOUND | 0 | 21 | evidence_89 |
| case_102 | user_100 | NO_PRIMARY_LINK_FOUND | 2 | 21 | evidence_89 |
| case_103 | user_101 | NO_PRIMARY_LINK_FOUND | 0 | 20 | evidence_10 |
| case_104 | user_102 | NO_PRIMARY_LINK_FOUND | 0 | 20 | evidence_10 |
| case_106 | user_104 | NO_PRIMARY_LINK_FOUND | 0 | 20 | evidence_10 |
| case_107 | user_105 | NO_PRIMARY_LINK_FOUND | 2 | 20 | evidence_10 |
| case_108 | user_106 | NO_PRIMARY_LINK_FOUND | 0 | 20 | evidence_10 |
| case_109 | user_107 | NO_PRIMARY_LINK_FOUND | 0 | 20 | evidence_10 |
| case_110 | user_108 | NO_PRIMARY_LINK_FOUND | 4 | 20 | evidence_10 |
| case_111 | user_109 | NO_PRIMARY_LINK_FOUND | 0 | 20 | evidence_10 |
| case_112 | user_110 | NO_PRIMARY_LINK_FOUND | 2 | 20 | evidence_10 |
| case_114 | user_112 | PRIMARY_LINK_ONLY_AFTER_CUTOFF | 0 | 20 | evidence_88 |
| case_116 | user_114 | PRIMARY_LINK_ONLY_AFTER_CUTOFF | 0 | 20 | evidence_88 |
| case_118 | user_116 | PRIMARY_LINK_ONLY_AFTER_CUTOFF | 4 | 20 | evidence_88 |
| case_119 | user_117 | PRIMARY_LINK_ONLY_AFTER_CUTOFF | 0 | 20 | evidence_88 |
| case_120 | user_118 | PRIMARY_LINK_ONLY_AFTER_CUTOFF | 0 | 20 | evidence_88 |
| case_122 | user_120 | PRIMARY_LINK_ONLY_AFTER_CUTOFF | 2 | 20 | evidence_88 |
| case_123 | user_121 | NO_PRIMARY_LINK_FOUND | 0 | 20 | evidence_87 |
| case_124 | user_122 | NO_PRIMARY_LINK_FOUND | 0 | 20 | evidence_87 |
| case_125 | user_123 | NO_PRIMARY_LINK_FOUND | 4 | 20 | evidence_87 |
| case_126 | user_124 | PRIMARY_LINK_ONLY_AFTER_CUTOFF | 0 | 20 | evidence_87 |
| case_127 | user_125 | PRIMARY_LINK_ONLY_AFTER_CUTOFF | 2 | 20 | evidence_87 |
| case_128 | user_126 | NO_PRIMARY_LINK_FOUND | 0 | 20 | evidence_87 |
| case_130 | user_128 | NO_PRIMARY_LINK_FOUND | 0 | 20 | evidence_87 |
| case_131 | user_129 | NO_PRIMARY_LINK_FOUND | 0 | 20 | evidence_87 |
| case_132 | user_130 | NO_PRIMARY_LINK_FOUND | 2 | 20 | evidence_87 |
| case_143 | user_141 | NO_PRIMARY_LINK_FOUND | 4 | 20 | evidence_86 |
| case_144 | user_142 | NO_PRIMARY_LINK_FOUND | 0 | 20 | evidence_86 |
| case_145 | user_143 | NO_PRIMARY_LINK_FOUND | 0 | 20 | evidence_86 |
| case_146 | user_144 | NO_PRIMARY_LINK_FOUND | 0 | 20 | evidence_86 |
| case_147 | user_145 | NO_PRIMARY_LINK_FOUND | 2 | 20 | evidence_86 |
| case_148 | user_146 | NO_PRIMARY_LINK_FOUND | 4 | 20 | evidence_86 |
| case_149 | user_147 | NO_PRIMARY_LINK_FOUND | 0 | 20 | evidence_86 |
| case_150 | user_148 | NO_PRIMARY_LINK_FOUND | 0 | 20 | evidence_86 |
| case_151 | user_149 | NO_PRIMARY_LINK_FOUND | 0 | 20 | evidence_86 |
| case_152 | user_150 | NO_PRIMARY_LINK_FOUND | 4 | 20 | evidence_86 |
| case_154 | user_152 | NO_PRIMARY_LINK_FOUND | 0 | 17 | evidence_15 |
| case_155 | user_153 | NO_PRIMARY_LINK_FOUND | 4 | 17 | evidence_15 |
| case_156 | user_154 | NO_PRIMARY_LINK_FOUND | 0 | 17 | evidence_15 |
| case_157 | user_155 | NO_PRIMARY_LINK_FOUND | 2 | 17 | evidence_15 |
| case_158 | user_156 | NO_PRIMARY_LINK_FOUND | 0 | 17 | evidence_15 |
| case_159 | user_157 | NO_PRIMARY_LINK_FOUND | 4 | 17 | evidence_15 |
| case_160 | user_158 | NO_PRIMARY_LINK_FOUND | 4 | 17 | evidence_15 |
| case_161 | user_159 | NO_PRIMARY_LINK_FOUND | 4 | 17 | evidence_15 |
| case_162 | user_160 | NO_PRIMARY_LINK_FOUND | 2 | 17 | evidence_15 |
| case_166 | user_164 | PRIMARY_LINK_ONLY_AFTER_CUTOFF | 0 | 17 | evidence_85 |
| case_168 | user_166 | PRIMARY_LINK_ONLY_AFTER_CUTOFF | 0 | 17 | evidence_85 |
| case_169 | user_167 | PRIMARY_LINK_ONLY_AFTER_CUTOFF | 0 | 17 | evidence_85 |
| case_171 | user_169 | PRIMARY_LINK_ONLY_AFTER_CUTOFF | 0 | 17 | evidence_85 |
| case_172 | user_170 | PRIMARY_LINK_ONLY_AFTER_CUTOFF | 2 | 17 | evidence_85 |
| case_173 | user_171 | NO_PRIMARY_LINK_FOUND | 0 | 17 | evidence_84 |
| case_174 | user_172 | NO_PRIMARY_LINK_FOUND | 0 | 17 | evidence_84 |
| case_175 | user_173 | PRIMARY_LINK_ONLY_AFTER_CUTOFF | 4 | 17 | evidence_84 |
| case_176 | user_174 | NO_PRIMARY_LINK_FOUND | 0 | 17 | evidence_84 |
| case_178 | user_176 | NO_PRIMARY_LINK_FOUND | 0 | 17 | evidence_84 |
| case_179 | user_177 | NO_PRIMARY_LINK_FOUND | 0 | 17 | evidence_84 |
| case_180 | user_178 | NO_PRIMARY_LINK_FOUND | 0 | 17 | evidence_84 |
| case_181 | user_179 | NO_PRIMARY_LINK_FOUND | 0 | 17 | evidence_84 |
| case_182 | user_180 | NO_PRIMARY_LINK_FOUND | 2 | 17 | evidence_84 |
| case_183 | user_181 | NO_PRIMARY_LINK_FOUND | 0 | 17 | evidence_83 |
| case_184 | user_182 | NO_PRIMARY_LINK_FOUND | 0 | 17 | evidence_83 |
| case_185 | user_183 | NO_PRIMARY_LINK_FOUND | 4 | 17 | evidence_83 |
| case_186 | user_184 | NO_PRIMARY_LINK_FOUND | 0 | 17 | evidence_83 |
| case_188 | user_186 | NO_PRIMARY_LINK_FOUND | 4 | 17 | evidence_83 |
| case_190 | user_188 | NO_PRIMARY_LINK_FOUND | 0 | 17 | evidence_83 |
| case_191 | user_189 | NO_PRIMARY_LINK_FOUND | 0 | 17 | evidence_83 |
| case_192 | user_190 | NO_PRIMARY_LINK_FOUND | 2 | 17 | evidence_83 |
| case_194 | user_192 | NO_PRIMARY_LINK_FOUND | 4 | 14 | evidence_82 |
| case_197 | user_195 | NO_PRIMARY_LINK_FOUND | 2 | 14 | evidence_82 |
| case_198 | user_196 | NO_PRIMARY_LINK_FOUND | 0 | 14 | evidence_82 |
| case_200 | user_198 | NO_PRIMARY_LINK_FOUND | 0 | 14 | evidence_82 |
| case_203 | user_201 | NO_PRIMARY_LINK_FOUND | 0 | 14 | evidence_20 |
| case_204 | user_202 | NO_PRIMARY_LINK_FOUND | 0 | 14 | evidence_20 |
| case_205 | user_203 | NO_PRIMARY_LINK_FOUND | 0 | 14 | evidence_20 |
| case_206 | user_204 | NO_PRIMARY_LINK_FOUND | 4 | 14 | evidence_20 |
| case_207 | user_205 | NO_PRIMARY_LINK_FOUND | 2 | 14 | evidence_20 |
| case_208 | user_206 | NO_PRIMARY_LINK_FOUND | 0 | 14 | evidence_20 |
| case_209 | user_207 | NO_PRIMARY_LINK_FOUND | 0 | 14 | evidence_20 |
| case_210 | user_208 | NO_PRIMARY_LINK_FOUND | 0 | 14 | evidence_20 |
| case_212 | user_210 | NO_PRIMARY_LINK_FOUND | 2 | 14 | evidence_20 |
| case_213 | user_211 | PRIMARY_LINK_ONLY_AFTER_CUTOFF | 0 | 14 | evidence_81 |
| case_214 | user_212 | PRIMARY_LINK_ONLY_AFTER_CUTOFF | 0 | 14 | evidence_81 |
| case_215 | user_213 | PRIMARY_LINK_ONLY_AFTER_CUTOFF | 0 | 14 | evidence_81 |
| case_216 | user_214 | PRIMARY_LINK_ONLY_AFTER_CUTOFF | 4 | 14 | evidence_81 |
| case_217 | user_215 | PRIMARY_LINK_ONLY_AFTER_CUTOFF | 2 | 14 | evidence_81 |
| case_218 | user_216 | PRIMARY_LINK_ONLY_AFTER_CUTOFF | 0 | 14 | evidence_81 |
| case_219 | user_217 | PRIMARY_LINK_ONLY_AFTER_CUTOFF | 0 | 14 | evidence_81 |
| case_220 | user_218 | PRIMARY_LINK_ONLY_AFTER_CUTOFF | 4 | 14 | evidence_81 |
| case_221 | user_219 | PRIMARY_LINK_ONLY_AFTER_CUTOFF | 0 | 14 | evidence_81 |
| case_222 | user_220 | PRIMARY_LINK_ONLY_AFTER_CUTOFF | 2 | 14 | evidence_81 |
| case_224 | user_222 | NO_PRIMARY_LINK_FOUND | 0 | 15 | evidence_80 |
| case_225 | user_223 | NO_PRIMARY_LINK_FOUND | 0 | 15 | evidence_80 |
| case_226 | user_224 | NO_PRIMARY_LINK_FOUND | 0 | 15 | evidence_80 |
| case_227 | user_225 | NO_PRIMARY_LINK_FOUND | 4 | 15 | evidence_80 |
| case_228 | user_226 | NO_PRIMARY_LINK_FOUND | 0 | 15 | evidence_80 |
| case_229 | user_227 | NO_PRIMARY_LINK_FOUND | 0 | 15 | evidence_80 |
| case_230 | user_228 | NO_PRIMARY_LINK_FOUND | 0 | 15 | evidence_80 |
| case_231 | user_229 | PRIMARY_LINK_ONLY_AFTER_CUTOFF | 0 | 15 | evidence_80 |
| case_232 | user_230 | NO_PRIMARY_LINK_FOUND | 2 | 15 | evidence_80 |
| case_234 | user_232 | PRIMARY_LINK_ONLY_AFTER_CUTOFF | 0 | 12 | evidence_79 |
| case_236 | user_234 | PRIMARY_LINK_ONLY_AFTER_CUTOFF | 0 | 12 | evidence_79 |
| case_240 | user_238 | PRIMARY_LINK_ONLY_AFTER_CUTOFF | 4 | 12 | evidence_79 |
| case_241 | user_239 | PRIMARY_LINK_ONLY_AFTER_CUTOFF | 4 | 12 | evidence_79 |
| case_242 | user_240 | PRIMARY_LINK_ONLY_AFTER_CUTOFF | 4 | 12 | evidence_79 |
| case_243 | user_241 | NO_PRIMARY_LINK_FOUND | 0 | 12 | evidence_78 |
| case_244 | user_242 | NO_PRIMARY_LINK_FOUND | 0 | 12 | evidence_78 |
| case_245 | user_243 | NO_PRIMARY_LINK_FOUND | 0 | 12 | evidence_78 |
| case_246 | user_244 | NO_PRIMARY_LINK_FOUND | 0 | 12 | evidence_78 |
| case_248 | user_246 | NO_PRIMARY_LINK_FOUND | 0 | 12 | evidence_78 |
| case_250 | user_248 | NO_PRIMARY_LINK_FOUND | 0 | 12 | evidence_78 |
| case_251 | user_249 | NO_PRIMARY_LINK_FOUND | 0 | 12 | evidence_78 |
| case_252 | user_250 | NO_PRIMARY_LINK_FOUND | 4 | 12 | evidence_78 |
| case_253 | user_251 | NO_PRIMARY_LINK_FOUND | 0 | 12 | evidence_24 |
| case_254 | user_252 | NO_PRIMARY_LINK_FOUND | 0 | 12 | evidence_24 |
| case_255 | user_253 | NO_PRIMARY_LINK_FOUND | 0 | 12 | evidence_24 |
| case_256 | user_254 | NO_PRIMARY_LINK_FOUND | 0 | 12 | evidence_24 |
| case_257 | user_255 | NO_PRIMARY_LINK_FOUND | 2 | 12 | evidence_24 |
| case_258 | user_256 | NO_PRIMARY_LINK_FOUND | 0 | 12 | evidence_24 |
| case_260 | user_258 | NO_PRIMARY_LINK_FOUND | 0 | 12 | evidence_24 |
| case_262 | user_260 | NO_PRIMARY_LINK_FOUND | 2 | 12 | evidence_24 |
| case_274 | user_272 | NO_PRIMARY_LINK_FOUND | 4 | 12 | evidence_77 |
| case_275 | user_273 | NO_PRIMARY_LINK_FOUND | 4 | 12 | evidence_77 |
| case_276 | user_274 | NO_PRIMARY_LINK_FOUND | 0 | 12 | evidence_77 |
| case_277 | user_275 | NO_PRIMARY_LINK_FOUND | 2 | 12 | evidence_77 |
| case_278 | user_276 | NO_PRIMARY_LINK_FOUND | 0 | 12 | evidence_77 |
| case_279 | user_277 | NO_PRIMARY_LINK_FOUND | 0 | 12 | evidence_77 |
| case_280 | user_278 | NO_PRIMARY_LINK_FOUND | 0 | 12 | evidence_77 |
| case_281 | user_279 | NO_PRIMARY_LINK_FOUND | 0 | 12 | evidence_77 |
| case_282 | user_280 | NO_PRIMARY_LINK_FOUND | 2 | 12 | evidence_77 |
| case_284 | user_282 | NO_PRIMARY_LINK_FOUND | 4 | 9 | evidence_76 |
| case_287 | user_285 | NO_PRIMARY_LINK_FOUND | 2 | 9 | evidence_76 |
| case_288 | user_286 | NO_PRIMARY_LINK_FOUND | 4 | 9 | evidence_76 |
| case_289 | user_287 | NO_PRIMARY_LINK_FOUND | 0 | 9 | evidence_76 |
| case_290 | user_288 | NO_PRIMARY_LINK_FOUND | 0 | 9 | evidence_76 |
| case_291 | user_289 | NO_PRIMARY_LINK_FOUND | 0 | 9 | evidence_76 |
| case_293 | user_291 | NO_PRIMARY_LINK_FOUND | 0 | 9 | evidence_75 |
| case_294 | user_292 | NO_PRIMARY_LINK_FOUND | 0 | 9 | evidence_75 |
| case_295 | user_293 | NO_PRIMARY_LINK_FOUND | 0 | 9 | evidence_75 |
| case_296 | user_294 | NO_PRIMARY_LINK_FOUND | 0 | 9 | evidence_75 |
| case_297 | user_295 | NO_PRIMARY_LINK_FOUND | 2 | 9 | evidence_75 |
| case_298 | user_296 | NO_PRIMARY_LINK_FOUND | 4 | 9 | evidence_75 |
| case_299 | user_297 | NO_PRIMARY_LINK_FOUND | 0 | 9 | evidence_75 |
| case_300 | user_298 | NO_PRIMARY_LINK_FOUND | 0 | 9 | evidence_75 |
| case_301 | user_299 | NO_PRIMARY_LINK_FOUND | 0 | 9 | evidence_75 |
| case_302 | user_300 | NO_PRIMARY_LINK_FOUND | 2 | 9 | evidence_75 |
| case_303 | user_301 | NO_PRIMARY_LINK_FOUND | 4 | 9 | evidence_29 |
| case_304 | user_302 | NO_PRIMARY_LINK_FOUND | 0 | 9 | evidence_29 |
| case_305 | user_303 | NO_PRIMARY_LINK_FOUND | 0 | 9 | evidence_29 |
| case_306 | user_304 | NO_PRIMARY_LINK_FOUND | 0 | 9 | evidence_29 |
| case_308 | user_306 | NO_PRIMARY_LINK_FOUND | 0 | 9 | evidence_29 |
| case_309 | user_307 | NO_PRIMARY_LINK_FOUND | 0 | 9 | evidence_29 |
| case_310 | user_308 | NO_PRIMARY_LINK_FOUND | 0 | 9 | evidence_29 |
| case_311 | user_309 | NO_PRIMARY_LINK_FOUND | 4 | 9 | evidence_29 |
| case_312 | user_310 | NO_PRIMARY_LINK_FOUND | 2 | 9 | evidence_29 |
| case_313 | user_311 | PRIMARY_LINK_ONLY_AFTER_CUTOFF | 0 | 13 | evidence_74 |
| case_314 | user_312 | PRIMARY_LINK_ONLY_AFTER_CUTOFF | 0 | 13 | evidence_74 |
| case_315 | user_313 | PRIMARY_LINK_ONLY_AFTER_CUTOFF | 0 | 13 | evidence_74 |
| case_316 | user_314 | PRIMARY_LINK_ONLY_AFTER_CUTOFF | 0 | 13 | evidence_74 |
| case_317 | user_315 | PRIMARY_LINK_ONLY_AFTER_CUTOFF | 2 | 13 | evidence_74 |
| case_318 | user_316 | PRIMARY_LINK_ONLY_AFTER_CUTOFF | 0 | 13 | evidence_74 |
| case_319 | user_317 | PRIMARY_LINK_ONLY_AFTER_CUTOFF | 0 | 13 | evidence_74 |
| case_320 | user_318 | PRIMARY_LINK_ONLY_AFTER_CUTOFF | 0 | 13 | evidence_74 |
| case_321 | user_319 | PRIMARY_LINK_ONLY_AFTER_CUTOFF | 4 | 13 | evidence_74 |
| case_322 | user_320 | PRIMARY_LINK_ONLY_AFTER_CUTOFF | 2 | 13 | evidence_74 |
| case_325 | user_323 | NO_PRIMARY_LINK_FOUND | 4 | 9 | evidence_73 |
| case_328 | user_326 | NO_PRIMARY_LINK_FOUND | 0 | 9 | evidence_73 |
| case_329 | user_327 | NO_PRIMARY_LINK_FOUND | 0 | 9 | evidence_73 |
| case_330 | user_328 | NO_PRIMARY_LINK_FOUND | 4 | 9 | evidence_73 |
| case_332 | user_330 | NO_PRIMARY_LINK_FOUND | 2 | 9 | evidence_73 |
| case_334 | user_332 | PRIMARY_LINK_ONLY_AFTER_CUTOFF | 0 | 9 | evidence_72 |
| case_335 | user_333 | PRIMARY_LINK_ONLY_AFTER_CUTOFF | 4 | 9 | evidence_72 |
| case_336 | user_334 | PRIMARY_LINK_ONLY_AFTER_CUTOFF | 0 | 9 | evidence_72 |
| case_337 | user_335 | PRIMARY_LINK_ONLY_AFTER_CUTOFF | 4 | 9 | evidence_72 |
| case_338 | user_336 | PRIMARY_LINK_ONLY_AFTER_CUTOFF | 0 | 9 | evidence_72 |
| case_339 | user_337 | PRIMARY_LINK_ONLY_AFTER_CUTOFF | 0 | 9 | evidence_72 |
| case_340 | user_338 | PRIMARY_LINK_ONLY_AFTER_CUTOFF | 0 | 9 | evidence_72 |
| case_341 | user_339 | PRIMARY_LINK_ONLY_AFTER_CUTOFF | 0 | 9 | evidence_72 |
| case_342 | user_340 | PRIMARY_LINK_ONLY_AFTER_CUTOFF | 2 | 9 | evidence_72 |
| case_343 | user_341 | NO_PRIMARY_LINK_FOUND | 0 | 9 | evidence_71 |
| case_344 | user_342 | NO_PRIMARY_LINK_FOUND | 4 | 9 | evidence_71 |
| case_345 | user_343 | NO_PRIMARY_LINK_FOUND | 0 | 9 | evidence_71 |
| case_346 | user_344 | NO_PRIMARY_LINK_FOUND | 0 | 9 | evidence_71 |
| case_347 | user_345 | NO_PRIMARY_LINK_FOUND | 2 | 9 | evidence_71 |
| case_348 | user_346 | NO_PRIMARY_LINK_FOUND | 0 | 9 | evidence_71 |
| case_349 | user_347 | NO_PRIMARY_LINK_FOUND | 0 | 9 | evidence_71 |
| case_350 | user_348 | NO_PRIMARY_LINK_FOUND | 0 | 9 | evidence_71 |
| case_351 | user_349 | NO_PRIMARY_LINK_FOUND | 0 | 9 | evidence_71 |
| case_352 | user_350 | NO_PRIMARY_LINK_FOUND | 2 | 9 | evidence_71 |
| case_353 | user_351 | NO_PRIMARY_LINK_FOUND | 0 | 5 | evidence_33 |
| case_354 | user_352 | NO_PRIMARY_LINK_FOUND | 0 | 5 | evidence_33 |
| case_356 | user_354 | NO_PRIMARY_LINK_FOUND | 0 | 5 | evidence_33 |
| case_358 | user_356 | NO_PRIMARY_LINK_FOUND | 0 | 5 | evidence_33 |
| case_359 | user_357 | NO_PRIMARY_LINK_FOUND | 0 | 5 | evidence_33 |
| case_360 | user_358 | NO_PRIMARY_LINK_FOUND | 4 | 5 | evidence_33 |
| case_361 | user_359 | NO_PRIMARY_LINK_FOUND | 0 | 5 | evidence_33 |
| case_362 | user_360 | NO_PRIMARY_LINK_FOUND | 2 | 5 | evidence_33 |
| case_373 | user_371 | NO_PRIMARY_LINK_FOUND | 4 | 5 | evidence_70 |
| case_376 | user_374 | NO_PRIMARY_LINK_FOUND | 4 | 5 | evidence_70 |
| case_377 | user_375 | NO_PRIMARY_LINK_FOUND | 2 | 5 | evidence_70 |
| case_382 | user_380 | NO_PRIMARY_LINK_FOUND | 2 | 5 | evidence_70 |
| case_393 | user_391 | NO_PRIMARY_LINK_FOUND | 0 | 5 | evidence_69 |
| case_394 | user_392 | NO_PRIMARY_LINK_FOUND | 0 | 5 | evidence_69 |
| case_395 | user_393 | NO_PRIMARY_LINK_FOUND | 0 | 5 | evidence_69 |
| case_396 | user_394 | NO_PRIMARY_LINK_FOUND | 0 | 5 | evidence_69 |
| case_397 | user_395 | NO_PRIMARY_LINK_FOUND | 2 | 5 | evidence_69 |
| case_398 | user_396 | NO_PRIMARY_LINK_FOUND | 0 | 5 | evidence_69 |
| case_399 | user_397 | NO_PRIMARY_LINK_FOUND | 0 | 5 | evidence_69 |
| case_400 | user_398 | NO_PRIMARY_LINK_FOUND | 0 | 5 | evidence_69 |
| case_401 | user_399 | NO_PRIMARY_LINK_FOUND | 0 | 5 | evidence_69 |
| case_402 | user_400 | NO_PRIMARY_LINK_FOUND | 2 | 5 | evidence_69 |
| case_403 | user_401 | NO_PRIMARY_LINK_FOUND | 0 | 5 | evidence_38 |
| case_404 | user_402 | NO_PRIMARY_LINK_FOUND | 0 | 5 | evidence_38 |
| case_406 | user_404 | NO_PRIMARY_LINK_FOUND | 4 | 5 | evidence_38 |
| case_407 | user_405 | NO_PRIMARY_LINK_FOUND | 2 | 5 | evidence_38 |
| case_408 | user_406 | NO_PRIMARY_LINK_FOUND | 0 | 5 | evidence_38 |
| case_409 | user_407 | NO_PRIMARY_LINK_FOUND | 0 | 5 | evidence_38 |
| case_410 | user_408 | NO_PRIMARY_LINK_FOUND | 0 | 5 | evidence_38 |
| case_411 | user_409 | NO_PRIMARY_LINK_FOUND | 0 | 5 | evidence_38 |
| case_412 | user_410 | NO_PRIMARY_LINK_FOUND | 2 | 5 | evidence_38 |
| case_423 | user_421 | PRIMARY_LINK_ONLY_AFTER_CUTOFF | 0 | 7 | evidence_68 |
| case_424 | user_422 | NO_PRIMARY_LINK_FOUND | 0 | 7 | evidence_68 |
| case_425 | user_423 | NO_PRIMARY_LINK_FOUND | 4 | 7 | evidence_68 |
| case_426 | user_424 | NO_PRIMARY_LINK_FOUND | 4 | 7 | evidence_68 |
| case_427 | user_425 | NO_PRIMARY_LINK_FOUND | 4 | 7 | evidence_68 |
| case_428 | user_426 | NO_PRIMARY_LINK_FOUND | 0 | 7 | evidence_68 |
| case_430 | user_428 | PRIMARY_LINK_ONLY_AFTER_CUTOFF | 0 | 7 | evidence_68 |
| case_431 | user_429 | NO_PRIMARY_LINK_FOUND | 0 | 7 | evidence_68 |
| case_432 | user_430 | NO_PRIMARY_LINK_FOUND | 2 | 7 | evidence_68 |
| case_443 | user_441 | NO_PRIMARY_LINK_FOUND | 0 | 3 | evidence_66 |
| case_444 | user_442 | NO_PRIMARY_LINK_FOUND | 0 | 3 | evidence_66 |
| case_445 | user_443 | NO_PRIMARY_LINK_FOUND | 4 | 3 | evidence_66 |
| case_446 | user_444 | NO_PRIMARY_LINK_FOUND | 0 | 3 | evidence_66 |
| case_447 | user_445 | NO_PRIMARY_LINK_FOUND | 4 | 3 | evidence_66 |
| case_448 | user_446 | NO_PRIMARY_LINK_FOUND | 0 | 3 | evidence_66 |
| case_449 | user_447 | NO_PRIMARY_LINK_FOUND | 0 | 3 | evidence_66 |
| case_450 | user_448 | NO_PRIMARY_LINK_FOUND | 0 | 3 | evidence_66 |
| case_451 | user_449 | NO_PRIMARY_LINK_FOUND | 4 | 3 | evidence_66 |
| case_452 | user_450 | NO_PRIMARY_LINK_FOUND | 2 | 3 | evidence_66 |
| case_454 | user_452 | NO_PRIMARY_LINK_FOUND | 0 | 3 | evidence_43 |
| case_455 | user_453 | NO_PRIMARY_LINK_FOUND | 0 | 3 | evidence_43 |
| case_456 | user_454 | NO_PRIMARY_LINK_FOUND | 0 | 3 | evidence_43 |
| case_457 | user_455 | NO_PRIMARY_LINK_FOUND | 2 | 3 | evidence_43 |
| case_458 | user_456 | NO_PRIMARY_LINK_FOUND | 0 | 3 | evidence_43 |
| case_459 | user_457 | NO_PRIMARY_LINK_FOUND | 0 | 3 | evidence_43 |
| case_460 | user_458 | NO_PRIMARY_LINK_FOUND | 0 | 3 | evidence_43 |
| case_461 | user_459 | NO_PRIMARY_LINK_FOUND | 0 | 3 | evidence_43 |
| case_462 | user_460 | NO_PRIMARY_LINK_FOUND | 2 | 3 | evidence_43 |
| case_463 | user_461 | PRIMARY_LINK_ONLY_AFTER_CUTOFF | 0 | 7 | evidence_65 |
| case_464 | user_462 | PRIMARY_LINK_ONLY_AFTER_CUTOFF | 0 | 7 | evidence_65 |
| case_466 | user_464 | PRIMARY_LINK_ONLY_AFTER_CUTOFF | 4 | 7 | evidence_65 |
| case_467 | user_465 | PRIMARY_LINK_ONLY_AFTER_CUTOFF | 4 | 7 | evidence_65 |
| case_468 | user_466 | PRIMARY_LINK_ONLY_AFTER_CUTOFF | 0 | 7 | evidence_65 |
| case_469 | user_467 | PRIMARY_LINK_ONLY_AFTER_CUTOFF | 0 | 7 | evidence_65 |
| case_470 | user_468 | PRIMARY_LINK_ONLY_AFTER_CUTOFF | 0 | 7 | evidence_65 |
| case_471 | user_469 | PRIMARY_LINK_ONLY_AFTER_CUTOFF | 0 | 7 | evidence_65 |
| case_472 | user_470 | PRIMARY_LINK_ONLY_AFTER_CUTOFF | 2 | 7 | evidence_65 |
| case_473 | user_471 | NO_PRIMARY_LINK_FOUND | 0 | 3 | evidence_45 |
| case_474 | user_472 | NO_PRIMARY_LINK_FOUND | 0 | 3 | evidence_45 |
| case_476 | user_474 | NO_PRIMARY_LINK_FOUND | 0 | 3 | evidence_45 |
| case_478 | user_476 | NO_PRIMARY_LINK_FOUND | 0 | 3 | evidence_45 |
| case_479 | user_477 | NO_PRIMARY_LINK_FOUND | 0 | 3 | evidence_45 |
| case_480 | user_478 | NO_PRIMARY_LINK_FOUND | 0 | 3 | evidence_45 |
| case_481 | user_479 | NO_PRIMARY_LINK_FOUND | 0 | 3 | evidence_45 |
| case_482 | user_480 | NO_PRIMARY_LINK_FOUND | 2 | 3 | evidence_45 |
| case_483 | user_481 | PRIMARY_LINK_ONLY_AFTER_CUTOFF | 4 | 3 | evidence_64 |
| case_484 | user_482 | PRIMARY_LINK_ONLY_AFTER_CUTOFF | 0 | 3 | evidence_64 |
| case_485 | user_483 | PRIMARY_LINK_ONLY_AFTER_CUTOFF | 0 | 3 | evidence_64 |
| case_488 | user_486 | PRIMARY_LINK_ONLY_AFTER_CUTOFF | 0 | 3 | evidence_64 |
| case_490 | user_488 | PRIMARY_LINK_ONLY_AFTER_CUTOFF | 0 | 3 | evidence_64 |
| case_492 | user_490 | PRIMARY_LINK_ONLY_AFTER_CUTOFF | 2 | 3 | evidence_64 |
| case_493 | user_491 | NO_PRIMARY_LINK_FOUND | 0 | 3 | evidence_63 |
| case_494 | user_492 | NO_PRIMARY_LINK_FOUND | 0 | 3 | evidence_63 |
| case_495 | user_493 | NO_PRIMARY_LINK_FOUND | 0 | 3 | evidence_63 |
| case_496 | user_494 | NO_PRIMARY_LINK_FOUND | 0 | 3 | evidence_63 |
| case_497 | user_495 | NO_PRIMARY_LINK_FOUND | 2 | 3 | evidence_63 |
| case_498 | user_496 | NO_PRIMARY_LINK_FOUND | 4 | 3 | evidence_63 |
| case_500 | user_498 | NO_PRIMARY_LINK_FOUND | 0 | 3 | evidence_63 |
| case_502 | user_500 | NO_PRIMARY_LINK_FOUND | 2 | 3 | evidence_63 |
| case_503 | user_501 | NO_PRIMARY_LINK_FOUND | 0 | 3 | evidence_47 |
| case_504 | user_502 | NO_PRIMARY_LINK_FOUND | 0 | 3 | evidence_47 |
| case_505 | user_503 | NO_PRIMARY_LINK_FOUND | 0 | 3 | evidence_47 |
| case_506 | user_504 | NO_PRIMARY_LINK_FOUND | 0 | 3 | evidence_47 |
| case_507 | user_505 | NO_PRIMARY_LINK_FOUND | 2 | 3 | evidence_47 |
| case_508 | user_506 | NO_PRIMARY_LINK_FOUND | 0 | 3 | evidence_47 |
| case_509 | user_507 | NO_PRIMARY_LINK_FOUND | 0 | 3 | evidence_47 |
| case_510 | user_508 | NO_PRIMARY_LINK_FOUND | 0 | 3 | evidence_47 |
| case_512 | user_510 | NO_PRIMARY_LINK_FOUND | 2 | 3 | evidence_47 |
| case_524 | user_522 | NO_PRIMARY_LINK_FOUND | 0 | 3 | evidence_62 |
| case_526 | user_524 | NO_PRIMARY_LINK_FOUND | 0 | 3 | evidence_62 |
| case_527 | user_525 | NO_PRIMARY_LINK_FOUND | 2 | 3 | evidence_62 |
| case_528 | user_526 | NO_PRIMARY_LINK_FOUND | 0 | 3 | evidence_62 |
| case_529 | user_527 | NO_PRIMARY_LINK_FOUND | 0 | 3 | evidence_62 |
| case_530 | user_528 | NO_PRIMARY_LINK_FOUND | 4 | 3 | evidence_62 |
| case_531 | user_529 | NO_PRIMARY_LINK_FOUND | 0 | 3 | evidence_62 |
| case_532 | user_530 | NO_PRIMARY_LINK_FOUND | 4 | 3 | evidence_62 |
| case_543 | user_543 | NO_PRIMARY_LINK_FOUND | 0 | 27 | evidence_52 |
| case_544 | user_544 | NO_PRIMARY_LINK_FOUND | 0 | 27 | evidence_52 |
| case_545 | user_545 | NO_PRIMARY_LINK_FOUND | 2 | 27 | evidence_52 |
| case_546 | user_546 | NO_PRIMARY_LINK_FOUND | 0 | 27 | evidence_52 |
| case_547 | user_547 | NO_PRIMARY_LINK_FOUND | 0 | 27 | evidence_52 |
| case_548 | user_548 | NO_PRIMARY_LINK_FOUND | 0 | 27 | evidence_52 |
| case_549 | user_549 | NO_PRIMARY_LINK_FOUND | 0 | 27 | evidence_52 |
| case_550 | user_550 | NO_PRIMARY_LINK_FOUND | 2 | 27 | evidence_52 |

The unattributed-primary count is shared evidence available at that cutoff, not a list of resources attributed to that person. It cannot be resolved by choosing a nearby event or a matching numeric suffix.

## Later links excluded from predictions

- case_33: account_2373 / evidence_01 / available 2026-09-15T11:59:39+00:00
- case_35: account_8491 / evidence_01 / available 2026-09-15T11:59:39+00:00
- case_39: account_8926 / evidence_01 / available 2026-09-15T11:59:39+00:00
- case_46: account_4092 / evidence_01 / available 2026-09-15T11:59:39+00:00
- case_50: account_3270 / evidence_01 / available 2026-09-15T11:59:39+00:00
- case_52: account_2373 / evidence_01 / available 2026-09-15T11:59:39+00:00
- case_55: account_9494 / evidence_01 / available 2026-09-15T11:59:39+00:00
- case_64: account_565 / evidence_06 / available 2026-09-18T11:55:24+00:00
- case_65: account_5488 / evidence_06 / available 2026-09-18T11:55:24+00:00
- case_66: account_1602 / evidence_06 / available 2026-09-18T11:55:24+00:00
- case_68: account_902 / evidence_06 / available 2026-09-18T11:55:24+00:00
- case_69: account_6138 / evidence_06 / available 2026-09-18T11:55:24+00:00
- case_70: account_6633 / evidence_06 / available 2026-09-18T11:55:24+00:00
- case_71: account_1378 / evidence_06 / available 2026-09-18T11:55:24+00:00
- case_72: account_7643 / evidence_06 / available 2026-09-18T11:55:24+00:00
- case_114: account_4833 / evidence_11 / available 2026-08-24T13:56:43+00:00
- case_116: account_1823 / evidence_11 / available 2026-08-24T13:56:43+00:00
- case_118: account_5785 / evidence_11 / available 2026-08-24T13:56:43+00:00
- case_119: account_8058 / evidence_11 / available 2026-08-24T13:56:43+00:00
- case_120: account_8656 / evidence_11 / available 2026-08-24T13:56:43+00:00
- case_122: account_9580 / evidence_11 / available 2026-08-24T13:56:43+00:00
- case_126: account_8819 / evidence_12 / available 2026-08-19T10:00:00+00:00
- case_127: account_6805 / evidence_12 / available 2026-08-19T10:00:00+00:00
- case_166: account_1837 / evidence_16 / available 2026-07-30T08:53:12+00:00
- case_168: account_8748 / evidence_16 / available 2026-07-30T08:53:12+00:00
- case_169: account_7268 / evidence_16 / available 2026-07-30T08:53:12+00:00
- case_171: account_7947 / evidence_16 / available 2026-07-30T08:53:12+00:00
- case_172: account_5675 / evidence_16 / available 2026-07-30T08:53:12+00:00
- case_175: account_246 / evidence_17 / available 2026-07-25T15:00:00+00:00
- case_213: account_6674 / evidence_21 / available 2026-07-05T07:54:27+00:00
- case_214: account_4752 / evidence_21 / available 2026-07-05T07:54:27+00:00
- case_215: account_1956 / evidence_21 / available 2026-07-05T07:54:27+00:00
- case_216: account_9682 / evidence_21 / available 2026-07-05T07:54:27+00:00
- case_217: account_7030 / evidence_21 / available 2026-07-05T07:54:27+00:00
- case_218: account_4066 / evidence_21 / available 2026-07-05T07:54:27+00:00
- case_219: account_4678 / evidence_21 / available 2026-07-05T07:54:27+00:00
- case_220: account_1007 / evidence_21 / available 2026-07-05T07:54:27+00:00
- case_221: account_4512 / evidence_21 / available 2026-07-05T07:54:27+00:00
- case_222: account_7237 / evidence_21 / available 2026-07-05T07:54:27+00:00
- case_231: account_7324 / evidence_22 / available 2026-06-30T07:00:00+00:00
- case_234: account_2614 / evidence_22 / available 2026-06-30T07:00:00+00:00
- case_236: account_629 / evidence_22 / available 2026-06-30T07:00:00+00:00
- case_240: account_6013 / evidence_22 / available 2026-06-30T07:00:00+00:00
- case_241: account_1789 / evidence_22 / available 2026-06-30T07:00:00+00:00
- case_242: account_3905 / evidence_22 / available 2026-06-30T07:00:00+00:00
- case_313: account_8264 / evidence_30 / available 2026-05-16T11:58:25+00:00
- case_314: account_591 / evidence_30 / available 2026-05-16T11:58:25+00:00
- case_315: account_782 / evidence_30 / available 2026-05-16T11:58:25+00:00
- case_316: account_9523 / evidence_30 / available 2026-05-16T11:58:25+00:00
- case_317: account_1972 / evidence_30 / available 2026-05-16T11:58:25+00:00
- case_318: account_1530 / evidence_30 / available 2026-05-16T11:58:25+00:00
- case_319: account_2088 / evidence_30 / available 2026-05-16T11:58:25+00:00
- case_320: account_9178 / evidence_30 / available 2026-05-16T11:58:25+00:00
- case_321: account_3525 / evidence_30 / available 2026-05-16T11:58:25+00:00
- case_322: account_9354 / evidence_30 / available 2026-05-16T11:58:25+00:00
- case_334: account_2255 / evidence_31 / available 2026-05-11T11:00:00+00:00
- case_335: account_8892 / evidence_31 / available 2026-05-11T11:00:00+00:00
- case_336: account_2282 / evidence_31 / available 2026-05-11T11:00:00+00:00
- case_337: account_767 / evidence_31 / available 2026-05-11T11:00:00+00:00
- case_338: account_4231 / evidence_31 / available 2026-05-11T11:00:00+00:00
- case_339: account_1340 / evidence_31 / available 2026-05-11T11:00:00+00:00
- case_340: account_1015 / evidence_31 / available 2026-05-11T11:00:00+00:00
- case_341: account_4377 / evidence_31 / available 2026-05-11T11:00:00+00:00
- case_342: account_614 / evidence_31 / available 2026-05-11T11:00:00+00:00
- case_423: account_2420 / evidence_40 / available 2026-03-22T08:00:00+00:00
- case_430: account_6006 / evidence_40 / available 2026-03-22T08:00:00+00:00
- case_463: account_1698 / evidence_44 / available 2026-03-02T10:59:23+00:00
- case_464: account_2480 / evidence_44 / available 2026-03-02T10:59:23+00:00
- case_466: account_7503 / evidence_44 / available 2026-03-02T10:59:23+00:00
- case_467: account_2437 / evidence_44 / available 2026-03-02T10:59:23+00:00
- case_468: account_641 / evidence_44 / available 2026-03-02T10:59:23+00:00
- case_469: account_6645 / evidence_44 / available 2026-03-02T10:59:23+00:00
- case_470: account_7023 / evidence_44 / available 2026-03-02T10:59:23+00:00
- case_471: account_9034 / evidence_44 / available 2026-03-02T10:59:23+00:00
- case_472: account_1957 / evidence_44 / available 2026-03-02T10:59:23+00:00
- case_483: account_9398 / evidence_45 / available 2026-02-23T10:00:00+00:00
- case_484: account_2961 / evidence_45 / available 2026-02-23T10:00:00+00:00
- case_485: account_3378 / evidence_45 / available 2026-02-23T10:00:00+00:00
- case_488: account_1433 / evidence_45 / available 2026-02-23T10:00:00+00:00
- case_490: account_4036 / evidence_45 / available 2026-02-23T10:00:00+00:00
- case_492: account_3589 / evidence_45 / available 2026-02-23T10:00:00+00:00

## Unresolved state details

- case_46: tombstone_17: missing state fields
- case_55: backup_9287: missing state fields; No identity-linked primary account state

## Documents without a grounded resource mapping


## Remaining work

Resolve unattributed readbacks through an explicit eligible identity/resource mapping if one can be extracted. Inspect any new source formats before declaring the gap irreducible. Keep strict mode enabled when evidence completeness is required; `--strict` refuses to write a result with unresolved coverage. Existing default labels for these cases are conservative fallbacks, not evidence-backed findings.

Diagnostic runtime: 5.14 seconds. Public sample answers are not read by this tool.
