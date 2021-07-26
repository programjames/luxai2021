import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

x = np.array([[-0.009145718078670484, 0.4819552939906657, 0.4376046661314561, -0.2878680162426548, -0.5888708046118651, -0.6739922016936966, -0.6397672951923585, -0.27894377011017824, 2.2976987038171615, 0.7777420418318819, 0.6347513538638516, 0.3806640210076271, -0.08617393236886106, 2.0237465071288674, -0.3571309904174047, -0.6637081567131808, -0.663698891939486, -0.35710328969082816, 2.0237923632979284, -0.0861103839539441, 0.3807446187240249, 0.6348481834199653, 0.7778541213715862, 2.2978248931716436, -0.27880475720388276, -0.6396168781814087, -0.6738319210137966, -0.5887023050643805, -0.28769302916138884, 0.43778433944611805, 0.4821377960361133, -0.008962268189250722], [0.8426773467395634, 3.1799662896389975, 3.0986272087069437, 0.26324308443287237, -0.4957529728573533, -0.6595938344680015, -0.6622051778972331, -0.5085645206218103, 0.23137804321178201, 3.0526961898002334, 3.303423918214005, 2.6355005082728375, -0.13178383396154492, -0.28363084429218244, -0.6082974312347016, -0.6913571275029824, -0.6913480653105637, -0.6082703364852495, -0.2835859910175129, -0.13172167571853666, 2.6355793424757934, 3.30351862865135, 3.052805815918706, 0.23150147020776224, -0.5084285509830551, -0.6620580538580771, -0.6594370627619206, -0.4955881628113872, 0.26341424066905006, 3.0988029466679023, 3.1801447973293477, 0.8428567799004014], [3.364176013758538, 3.8533614136260184, 3.7222354022866924, 2.665902396342439, -0.22351031224953744, -0.6288426857041305, -0.6752147682822924, -0.5926050455447474, -0.10950602991715286, 2.860702878554253, 2.9268700392039104, 0.21217767019709788, -0.48569554109856483, -0.6118315940517629, -0.6737474888970123, -0.6948673418428228, -0.6948588785608791, -0.6737221847823474, -0.6117897054522867, -0.4856374920658588, 0.2122512914568282, 2.926958485922869, 2.86080525271986, -0.109390769272661, -0.5924780730416419, -0.6750773807858588, -0.6286962896219226, -0.2233564094062359, 2.666062224053128, 3.722399508352872, 3.8535281053481043, 3.3643435705943716], [0.9988283383093091, 3.4826033565895003, 3.119581186633063, 0.24882213921592822, -0.5027865246061438, -0.6653642278677898, -0.6940556250155028, -0.6691518050945351, -0.5464400019975959, -0.15867131374950172, -0.140727775632489, -0.49079374159171163, -0.634258275233238, -0.6713053781986282, -0.6797165932186289, -0.6811173080976509, -0.6811098134883089, -0.6796941855650545, -0.6712682850933334, -0.6342068732503439, -0.4907285527302614, -0.14064946183029264, -0.15858067118813923, -0.5463379528157234, -0.669039389133584, -0.69393399003326, -0.6652346184941331, -0.5026502697030608, 0.24896363806807287, 3.1197264731270096, 3.4827509309699067, 0.998976679427642], [0.4294715924064505, 2.6659589843942584, 0.24354472156049312, -0.44160743807495706, -0.639274854422407, -0.6896711505778252, -0.6991036838737772, -0.6958055351505816, -0.6709536302315993, -0.6151618868142696, -0.6110415273486902, -0.6604702174869708, -0.6852305347378778, -0.6836823216959456, -0.6757108440570576, -0.6721883921130463, -0.6721821931852183, -0.6756923105488042, -0.683651643719509, -0.6851880243171333, -0.6604163095524491, -0.6109767704685618, -0.6150869409075801, -0.6708692583781755, -0.6957125968978968, -0.699003127825959, -0.6895640049456492, -0.6391622171634896, -0.44149046688977833, 0.24366482411410928, 2.6660809789633717, 0.42959421880090787], [-0.07911538060105272, -0.1291759691633878, -0.4880601940668825, -0.6364660036725276, -0.6840597457156556, -0.6908698835905493, -0.6905229235862542, -0.6941028929436364, -0.6961435515761298, -0.69331211766041, -0.6973986350030561, -0.7050165712594545, -0.6983589041709095, -0.6799406512971249, -0.6718344268314826, -0.6768367666666162, -0.6768321329576157, -0.6718205737031173, -0.6799177236742313, -0.6983271380490947, -0.7049762955955874, -0.6973502630036652, -0.6932561438881581, -0.6960805476474459, -0.6940335006486755, -0.6904478500027764, -0.6907898950909424, -0.6839756611431269, -0.636378685524484, -0.4879705406744037, -0.12908490325807165, -0.07902384272224339], [2.0391325880296423, -0.2720089374732355, -0.6083004200142905, -0.6735270743587041, -0.6843812424533517, -0.6820558281453941, -0.6825372168778276, -0.6889540912778944, -0.6991819213334498, -0.709155288099014, -0.7155189436848062, -0.7065634716254507, -0.6679964056050451, -0.6078581969445356, -0.6078570092434514, -0.6587346043474671, -0.6587317361489351, -0.607848436081758, -0.6078440120237492, -0.6679767612966678, -0.706538578174797, -0.7154890626799073, -0.7091207285976484, -0.6991430380103392, -0.6889112805647581, -0.6824909133208781, -0.6820065020224035, -0.6843293966507353, -0.6734732388372944, -0.6082451466630061, -0.27195279478206036, 2.039189021575589], [-0.33211082294811867, -0.586015103864117, -0.6600974884751469, -0.6769350854446454, -0.6786940625643556, -0.6800997244848652, -0.6825826840782554, -0.6860823156883367, -0.7009089826207227, -0.7154221583672165, -0.7122616521704828, -0.6609322964270259, -0.5009673837295514, -0.14242319514866808, -0.1580957697757961, -0.522451423857087, -0.5224504428601944, -0.15809284052776973, -0.14241835776077694, -0.5009607025044103, -0.6609238566385702, -0.7122515540620924, -0.7154105146385685, -0.7008959152367762, -0.6860679575732842, -0.6825671781626674, -0.6800832242740285, -0.6786767321015308, -0.6769170973787144, -0.6600790245779802, -0.5859963519228266, -0.33209197431989246],
              [-0.6472033849388126, -0.6729025228422358, -0.6811160698792307, -0.6805920880952883, -0.682408967866607, -0.6842830070193955, -0.6711460625125589, -0.6388701384748803, -0.6770535136155011, -0.7076104861408723, -0.6885990446512738, -0.527026660770618, 0.1918749099475079, 2.908389103042458, 2.838386644941748, -0.07997818756329522, -0.07997913113352695, 2.838383818049598, 2.9083844049611027, 0.1918683638543408, -0.5270350171344758, -0.6886091497030202, -0.7076222519468907, -0.6770668252981089, -0.6388848584554001, -0.6711620348230696, -0.6843000605143672, -0.6824269190461436, -0.6806107450630208, -0.6811352356900144, -0.672921994684728, -0.6472229587089942], [-0.7029984413820785, -0.701364599818973, -0.6932521892232693, -0.6882107648745581, -0.6897965028959447, -0.6740336984797466, -0.5762299549405352, -0.26274080608202155, -0.5246132416839195, -0.6574793798947622, -0.6484444254294695, -0.2661722414927521, 2.5238305469200615, 3.1698975777086744, 2.876030255831548, -0.06090868865920207, -0.06091150820861735, 2.8760218182493666, 3.169883584474025, 2.523811101032214, -0.26619699041012046, -0.648474262516634, -0.6575140213112158, -0.5246523399119862, -0.2627839579456932, -0.5762767101659332, -0.6740835666902427, -0.6898489606621823, -0.6882652638732445, -0.6933081598668203, -0.7014214587657008, -0.7030555967580483], [-0.7177737020956805, -0.7116165624105903, -0.6994583772376757, -0.6943118253545286, -0.6909601937801604, -0.6247165606267266, -0.19772423653973448, 2.5271267646116167, 0.19676620404500111, -0.501953787063214, -0.6477750280214876, -0.565866933328699, -0.183636861772702, -0.05159123664505749, -0.10536435409047584, -0.43484007349090525, -0.43484463551445707, -0.10537800271329445, -0.051613862210105665, -0.18366829372245075, -0.5659069388170237, -0.647823254538439, -0.5020097663222152, 0.19670304063084165, 2.5270570710108835, -0.19779973354750702, -0.6247970706681976, -0.6910448760344785, -0.6943997957659995, -0.6995487194264527, -0.7117083369791146, -0.7178659561515168], [-0.7211323737987811, -0.7137912863083002, -0.7011731626043556, -0.6968708325103457, -0.6897867181118578, -0.595127387753088, -0.04492314497214389, 3.240150452257515, 2.9837092834584418, -0.11101887788315956, -0.5781603613531905, -0.5971141927538497, -0.5692703848160363, -0.5428172480058695, -0.47573038918006993, -0.19963285791966356, -0.19963895122588227, -0.4757486133573128, -0.5428474448696026, -0.5693123261738169, -0.5971676315331607, -0.5782248251478252, -0.11109372501249659, 2.983624825751857, 3.240057265023216, -0.04502408701205285, -0.5952350285414276, -0.6898999335722173, -0.6969884417258108, -0.7012939407970009, -0.7139139795910197, -0.7212557073430617], [-0.7132990373887296, -0.7048952505243875, -0.695894534455455, -0.6941545696606966, -0.6875908772354862, -0.5884996160328306, -0.01947700050708323, 3.3319114586768315, 3.3077402059280736, 0.0001376545892259884, -0.45349581773842296, -0.2376226700774584, -0.47915649349239864, -0.558288654839405, -0.25784593571203196, 2.3552194648164857, 2.355212115727003, -0.25786790388719716, -0.5583250100400292, -0.47920691254064174, -0.237687111799195, -0.45357366319595904, 4.722527516243247e-05, 3.307638148543713, 3.3317988478906955, -0.019598983046322127, -0.5886296931839752, -0.6877276890369828, -0.6942966904267323, -0.6960404852504851, -0.7050435150952268, -0.7134480755948758], [-0.6701868950239742, -0.649038904745808, -0.6698029291238399, -0.681699922470326, -0.6835839495374962, -0.6039742025525161, -0.10660598941614302, 2.9690201839669115, 2.9756589271727627, -0.024569545234314205, -0.10694801696441303, 2.497558603644908, 0.32596760325748875, -0.47058383141607507, -0.5409010281316071, -0.24242133430294466, -0.24242961922926476, -0.540925777305123, -0.4706246943193442, 0.3259114033241417, 2.497486035629347, -0.10703584313346326, -0.024671610736810123, 2.975543724068327, 2.968893062520891, -0.10674369156849856, -0.6041210428622765, -0.6837383926788014, -0.6818603592689989, -0.6699676895143725, -0.6492062758643726, -0.670355139314168], [-0.5125774576793134, -0.3220178598881098, -0.583066853321661, -0.65557011662818, -0.6771255677186581, -0.640337427347788, -0.4217063119851878, 0.31172411396785016, 0.3195466797713493, -0.3324006905942092, -0.0880672218046854, 2.8189330692019112, 2.5591900666811895, -0.2248103635755161, -0.6152217070827657, -0.6387721318354913, -0.6387810085973875, -0.6152482446817178, -0.2248542931859756, 2.5591291169149315, 2.8188551956294745, -0.0881612868303705, -0.3325099647412024, 0.3194233478989901, 0.3115880245108098, -0.4218537286106874, -0.6404946267814822, -0.6772909076014351, -0.6557418721347155, -0.5832432367825859, -0.3221970400526324, -0.5127575721620445], [0.006337277328960056, 2.0404178350163136, -0.3172337605248394, -0.6201866293863603, -0.6678926592049415, -0.6239478994526451, -0.22797234885886697, 2.5141119727394976, 2.517671269635077, -0.1675775663014072, -0.32684970101211874, 0.3564625169161957, 0.2854416192556961, -0.4412912594136138, -0.662016811184964, -0.707629397262604, -0.7076384772427531, -0.6620439645304916, -0.44133624503792745, 0.2853791291129859, 0.3563828306613672, -0.32694588803056845, -0.1676892840688744, 2.517545186945629, 2.5139728498932516, -0.22812305141194433, -0.6241086029671443, -0.6680616846472596, -0.6203622150013004, -0.31741407723287196, 2.0402346601493235, 0.006153146877856841]])
sns.heatmap(x, cmap='vlag')
plt.show()