MATCH (n) detach delete n;

CREATE
(_schema:_Schema {`description`:'the meta schema to label schemas',`_uid`:'meta1',`_schemaname`:'_Schema',`_techname`:'_Schema'}),
(_description:_Property {`description`:'longer description',`_scalartype`:'string',`_uid`:'meta2',`_techname`:'description'}),
(_techname:_Property {`description`:'internal scalar representation',`_scalartype`:'string',`_uid`:'meta3',`_techname`:'_techname'}),
(_prop:_Relation {`description`:'_Schema --_PROP-> _Property',`_targetarity`:'*',`_uid`:'meta5',`_sourcearity`:'*',`_techname`:'_PROP'}),
(_arity:_Property {`description`:'How often can there be the element',`_scalartype`:'string',`_uid`:'meta7',`_techname`:'_arity'}),
(_relation:_Schema {`description`:'used to define a type of relation',`_uid`:'meta8',`_schemaname`:'_Relation',`_techname`:'_Relation'}),
(_property:_Schema {`description`:'A description of  property of semantic meta object',`_uid`:'meta9',`_schemaname`:'_Property',`_techname`:'_Property'}),
(_scalartype:_Property {`description`:'Von welchem Typ ist der Wert',`_scalartype`:'string',`_uid`:'meta10',`_techname`:'_scalartype'}),
(_name:_Property {`description`:'full name of  thing',`_scalartype`:'string',`_uid`:'meta11',`_techname`:'name'}),
(_person:_Schema {`description`:'a human',`_uid`:'meta12',`_schemaname`:'Person',`_techname`:'Person'}),
(_firstname:_Property {`description`:'first name of a person',`_scalartype`:'string',`_uid`:'meta13',`_techname`:'firstname'}),
(_lastname:_Property {`description`:'last name of a person',`_scalartype`:'string',`_uid`:'meta14',`_techname`:'lastname'}),
(_likes:_Relation {`description`:'xoxoxo',`_targetarity`:'1',`_uid`:'meta15',`_sourcearity`:'?',`_techname`:'LIKES'}),
(_bob:Person {`name`:'Bob',`firstname`:'',`_uid`:'meta16',`lastname`:''}),
(_alice:Person {`name`:'Alice Alison',`firstname`:'Alice',`_uid`:'meta17',`lastname`:'Alison'}),
(_schemaname:_Property {`description`:'the name of a schema',`_scalartype`:'string',`_uid`:'meta18',`_techname`:'_schemaname'}),
(_sourcearity:_Property {`description`:'_arity of start',`_scalartype`:'string',`_uid`:'meta19',`_techname`:'_sourcearity'}),
(_targetarity:_Property {`description`:'_arity of target',`_scalartype`:'string',`_uid`:'meta20',`_techname`:'_targetarity'}),
(_source:_Relation {`description`:'schema for the start of relation',`_targetarity`:'*',`_uid`:'meta21',`_sourcearity`:'*',`_techname`:'_SOURCE'}),
(_target:_Relation {`description`:'schema for the start of relation',`_targetarity`:'*',`_uid`:'meta22',`_sourcearity`:'*',`_techname`:'_TARGET'}),
(_schema)-[:`_PROP` {`_uid`:'meta21',`_arity`:'1'}]->(_description),
(_schema)-[:`_PROP` {`_uid`:'meta22',`_arity`:'1'}]->(_techname),
(_prop)-[:`_SOURCE` {`_uid`:'meta23'}]->(_schema),
(_schema)-[:`_PROP` {`_uid`:'meta24',`_arity`:'1'}]->(_schemaname),
(_prop)-[:`_PROP` {`_uid`:'meta25',`_arity`:'1'}]->(_arity),
(_relation)-[:`_PROP` {`_uid`:'meta27',`_arity`:'1'}]->(_techname),
(_relation)-[:`_PROP` {`_uid`:'meta28',`_arity`:'1'}]->(_description),
(_relation)-[:`_PROP` {`_uid`:'meta30',`_arity`:'*'}]->(_sourcearity),
(_relation)-[:`_PROP` {`_uid`:'meta31',`_arity`:'*'}]->(_targetarity),
(_property)-[:`_PROP` {`_uid`:'meta32',`_arity`:'1'}]->(_scalartype),
(_property)-[:`_PROP` {`_uid`:'meta33',`_arity`:'1'}]->(_description),
(_property)-[:`_PROP` {`_uid`:'meta34',`_arity`:'1'}]->(_techname),
(_prop)-[:`_TARGET` {`_uid`:'meta35'}]->(_property),
(_person)-[:`_PROP` {`_uid`:'meta36',`_arity`:'?'}]->(_lastname),
(_person)-[:`_PROP` {`_uid`:'meta37',`_arity`:'?'}]->(_firstname),
(_person)-[:`_PROP` {`_uid`:'meta38',`_arity`:'1'}]->(_name),
(_likes)-[:`_SOURCE` {`_uid`:'meta39'}]->(_person),
(_likes)-[:`_TARGET` {`_uid`:'meta40'}]->(_person),
(_source)-[:`_SOURCE` {`_uid`:'meta41'}]->(_relation),
(_target)-[:`_SOURCE` {`_uid`:'meta42'}]->(_relation),
(_alice)-[:`LIKES` {`_uid`:'meta43'}]->(_bob),
(_bob)-[:`LIKES` {`_uid`:'meta44'}]->(_alice);