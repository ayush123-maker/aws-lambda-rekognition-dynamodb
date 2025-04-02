{\rtf1\ansi\ansicpg1252\cocoartf2821
\cocoatextscaling0\cocoaplatform0{\fonttbl\f0\fnil\fcharset0 Menlo-Regular;}
{\colortbl;\red255\green255\blue255;\red157\green0\blue210;\red255\green255\blue255;\red45\green45\blue45;
\red15\green112\blue1;\red0\green0\blue0;\red144\green1\blue18;\red101\green76\blue29;\red0\green0\blue255;
\red0\green0\blue109;\red19\green118\blue70;\red32\green108\blue135;}
{\*\expandedcolortbl;;\cssrgb\c68627\c0\c85882;\cssrgb\c100000\c100000\c100000;\cssrgb\c23137\c23137\c23137;
\cssrgb\c0\c50196\c0;\cssrgb\c0\c0\c0;\cssrgb\c63922\c8235\c8235;\cssrgb\c47451\c36863\c14902;\cssrgb\c0\c0\c100000;
\cssrgb\c0\c6275\c50196;\cssrgb\c3529\c52549\c34510;\cssrgb\c14902\c49804\c60000;}
\margl1440\margr1440\vieww11520\viewh8400\viewkind0
\deftab720
\pard\pardeftab720\partightenfactor0

\f0\fs24 \cf2 \cb3 \expnd0\expndtw0\kerning0
\outl0\strokewidth0 \strokec2 from\cf4 \strokec4  decimal \cf2 \strokec2 import\cf4 \strokec4  Decimal\cb1 \
\cf2 \cb3 \strokec2 import\cf4 \strokec4  boto3\cb1 \
\cf2 \cb3 \strokec2 import\cf4 \strokec4  json\cb1 \
\cf2 \cb3 \strokec2 import\cf4 \strokec4  os \cf5 \strokec5 # Added for environment variable\cf4 \cb1 \strokec4 \
\cf2 \cb3 \strokec2 import\cf4 \strokec4  urllib.parse \cf5 \strokec5 # Added for handling object keys with spaces/special chars\cf4 \cb1 \strokec4 \
\
\pard\pardeftab720\partightenfactor0
\cf5 \cb3 \strokec5 # Get the DynamoDB table name from environment variable for flexibility\cf4 \cb1 \strokec4 \
\pard\pardeftab720\partightenfactor0
\cf4 \cb3 TABLE_NAME \strokec6 =\strokec4  os.environ.get(\cf7 \strokec7 'DYNAMODB_TABLE'\cf4 \strokec4 , \cf7 \strokec7 'ImageAnalysisResults'\cf4 \strokec4 ) \cf5 \strokec5 # Default if not set\cf4 \cb1 \strokec4 \
\
\pard\pardeftab720\partightenfactor0
\cf5 \cb3 \strokec5 # Initialize AWS clients\cf4 \cb1 \strokec4 \
\cf5 \cb3 \strokec5 # It's good practice to initialize them outside the handler for potential reuse\cf4 \cb1 \strokec4 \
\pard\pardeftab720\partightenfactor0
\cf4 \cb3 s3_client \strokec6 =\strokec4  boto3.client(\cf7 \strokec7 's3'\cf4 \strokec4 )\cb1 \
\cb3 rekognition_client \strokec6 =\strokec4  boto3.client(\cf7 \strokec7 'rekognition'\cf4 \strokec4 )\cb1 \
\cb3 dynamodb \strokec6 =\strokec4  boto3.resource(\cf7 \strokec7 'dynamodb'\cf4 \strokec4 ) \cf5 \strokec5 # Using resource for simpler PutItem\cf4 \cb1 \strokec4 \
\cb3 table \strokec6 =\strokec4  dynamodb.Table(TABLE_NAME)\cb1 \
\
\pard\pardeftab720\partightenfactor0
\cf8 \cb3 \strokec8 print\cf4 \strokec4 (\cf9 \strokec9 f\cf7 \strokec7 "Lambda function initializing. Target DynamoDB Table: \cf9 \strokec9 \{\cf4 \strokec4 TABLE_NAME\cf9 \strokec9 \}\cf7 \strokec7 "\cf4 \strokec4 )\cb1 \
\
\pard\pardeftab720\partightenfactor0
\cf9 \cb3 \strokec9 def\cf4 \strokec4  \cf8 \strokec8 lambda_handler\cf4 \strokec4 (\cf10 \strokec10 event\cf4 \strokec4 , \cf10 \strokec10 context\cf4 \strokec4 ):\cb1 \
\pard\pardeftab720\partightenfactor0
\cf4 \cb3     \cf8 \strokec8 print\cf4 \strokec4 (\cf7 \strokec7 "Received event:"\cf4 \strokec4 , json.dumps(event, \cf10 \strokec10 indent\cf4 \strokec6 =\cf11 \strokec11 2\cf4 \strokec4 ))\cb1 \
\
\cb3     \cf5 \strokec5 # Get the bucket name and object key from the S3 event record\cf4 \cb1 \strokec4 \
\cb3     \cf2 \strokec2 try\cf4 \strokec4 :\cb1 \
\cb3         \cf5 \strokec5 # Handle potential URL encoding in object keys (e.g., spaces become '+')\cf4 \cb1 \strokec4 \
\cb3         bucket_name \strokec6 =\strokec4  event[\cf7 \strokec7 'Records'\cf4 \strokec4 ][\cf11 \strokec11 0\cf4 \strokec4 ][\cf7 \strokec7 's3'\cf4 \strokec4 ][\cf7 \strokec7 'bucket'\cf4 \strokec4 ][\cf7 \strokec7 'name'\cf4 \strokec4 ]\cb1 \
\cb3         object_key \strokec6 =\strokec4  urllib.parse.unquote_plus(event[\cf7 \strokec7 'Records'\cf4 \strokec4 ][\cf11 \strokec11 0\cf4 \strokec4 ][\cf7 \strokec7 's3'\cf4 \strokec4 ][\cf7 \strokec7 'object'\cf4 \strokec4 ][\cf7 \strokec7 'key'\cf4 \strokec4 ], \cf10 \strokec10 encoding\cf4 \strokec6 =\cf7 \strokec7 'utf-8'\cf4 \strokec4 )\cb1 \
\cb3         \cf8 \strokec8 print\cf4 \strokec4 (\cf9 \strokec9 f\cf7 \strokec7 "Processing object \cf9 \strokec9 \{\cf4 \strokec4 object_key\cf9 \strokec9 \}\cf7 \strokec7  from bucket \cf9 \strokec9 \{\cf4 \strokec4 bucket_name\cf9 \strokec9 \}\cf7 \strokec7 "\cf4 \strokec4 )\cb1 \
\cb3     \cf2 \strokec2 except\cf4 \strokec4  \cf12 \strokec12 KeyError\cf4 \strokec4  \cf2 \strokec2 as\cf4 \strokec4  e:\cb1 \
\cb3         \cf8 \strokec8 print\cf4 \strokec4 (\cf9 \strokec9 f\cf7 \strokec7 "Error extracting bucket/key from event: \cf9 \strokec9 \{\cf4 \strokec4 e\cf9 \strokec9 \}\cf7 \strokec7 "\cf4 \strokec4 )\cb1 \
\cb3         \cf8 \strokec8 print\cf4 \strokec4 (\cf7 \strokec7 "Full event:"\cf4 \strokec4 , json.dumps(event, \cf10 \strokec10 indent\cf4 \strokec6 =\cf11 \strokec11 2\cf4 \strokec4 ))\cb1 \
\cb3         \cf2 \strokec2 return\cf4 \strokec4  \{\cf7 \strokec7 'statusCode'\cf4 \strokec4 : \cf11 \strokec11 400\cf4 \strokec4 , \cf7 \strokec7 'body'\cf4 \strokec4 : \cf7 \strokec7 'Error parsing S3 event structure'\cf4 \strokec4 \}\cb1 \
\
\cb3     \cf2 \strokec2 try\cf4 \strokec4 :\cb1 \
\cb3         \cf5 \strokec5 # Call Rekognition to detect labels\cf4 \cb1 \strokec4 \
\cb3         \cf8 \strokec8 print\cf4 \strokec4 (\cf9 \strokec9 f\cf7 \strokec7 "Calling Rekognition DetectLabels for \cf9 \strokec9 \{\cf4 \strokec4 object_key\cf9 \strokec9 \}\cf7 \strokec7 ..."\cf4 \strokec4 )\cb1 \
\cb3         response \strokec6 =\strokec4  rekognition_client.detect_labels(\cb1 \
\cb3             \cf10 \strokec10 Image\cf4 \strokec6 =\strokec4 \{\cb1 \
\cb3                 \cf7 \strokec7 'S3Object'\cf4 \strokec4 : \{\cb1 \
\cb3                     \cf7 \strokec7 'Bucket'\cf4 \strokec4 : bucket_name,\cb1 \
\cb3                     \cf7 \strokec7 'Name'\cf4 \strokec4 : object_key\cb1 \
\cb3                 \}\cb1 \
\cb3             \},\cb1 \
\cb3             \cf10 \strokec10 MaxLabels\cf4 \strokec6 =\cf11 \strokec11 10\cf4 \strokec4 , \cf5 \strokec5 # Limit the number of labels returned\cf4 \cb1 \strokec4 \
\cb3             \cf10 \strokec10 MinConfidence\cf4 \strokec6 =\cf11 \strokec11 75\cf4 \strokec4  \cf5 \strokec5 # Only include labels with confidence >= 75%\cf4 \cb1 \strokec4 \
\cb3         )\cb1 \
\cb3         \cf8 \strokec8 print\cf4 \strokec4 (\cf7 \strokec7 "Rekognition response received."\cf4 \strokec4 )\cb1 \
\
\cb3         \cf5 \strokec5 # Extract label names\cf4 \cb1 \strokec4 \
\cb3         labels \strokec6 =\strokec4  [\{\cf7 \strokec7 'Name'\cf4 \strokec4 : label[\cf7 \strokec7 'Name'\cf4 \strokec4 ], \cf7 \strokec7 'Confidence'\cf4 \strokec4 : Decimal(\cf12 \strokec12 str\cf4 \strokec4 (\cf8 \strokec8 round\cf4 \strokec4 (label[\cf7 \strokec7 'Confidence'\cf4 \strokec4 ], \cf11 \strokec11 2\cf4 \strokec4 )))\} \cf2 \strokec2 for\cf4 \strokec4  label \cf2 \strokec2 in\cf4 \strokec4  response[\cf7 \strokec7 'Labels'\cf4 \strokec4 ]]\cb1 \
\cb3         \cf8 \strokec8 print\cf4 \strokec4 (\cf9 \strokec9 f\cf7 \strokec7 "Detected labels: \cf9 \strokec9 \{\cf4 \strokec4 labels\cf9 \strokec9 \}\cf7 \strokec7 "\cf4 \strokec4 )\cb1 \
\
\cb3         \cf5 \strokec5 # Store the results in DynamoDB\cf4 \cb1 \strokec4 \
\cb3         \cf8 \strokec8 print\cf4 \strokec4 (\cf9 \strokec9 f\cf7 \strokec7 "Storing results in DynamoDB table \cf9 \strokec9 \{\cf4 \strokec4 TABLE_NAME\cf9 \strokec9 \}\cf7 \strokec7 ..."\cf4 \strokec4 )\cb1 \
\cb3         db_response \strokec6 =\strokec4  table.put_item(\cb1 \
\cb3             \cf10 \strokec10 Item\cf4 \strokec6 =\strokec4 \{\cb1 \
\cb3                 \cf7 \strokec7 'ImageName'\cf4 \strokec4 : object_key, \cf5 \strokec5 # Partition Key\cf4 \cb1 \strokec4 \
\cb3                 \cf7 \strokec7 'Labels'\cf4 \strokec4 : labels,\cb1 \
\cb3                 \cf7 \strokec7 'Bucket'\cf4 \strokec4 : bucket_name \cf5 \strokec5 # Adding bucket name as extra info\cf4 \cb1 \strokec4 \
\cb3             \}\cb1 \
\cb3         )\cb1 \
\cb3         \cf8 \strokec8 print\cf4 \strokec4 (\cf7 \strokec7 "Successfully stored results in DynamoDB."\cf4 \strokec4 )\cb1 \
\cb3         \cf8 \strokec8 print\cf4 \strokec4 (\cf7 \strokec7 "DynamoDB put_item response:"\cf4 \strokec4 , db_response)\cb1 \
\
\cb3         \cf2 \strokec2 return\cf4 \strokec4  \{\cb1 \
\cb3             \cf7 \strokec7 'statusCode'\cf4 \strokec4 : \cf11 \strokec11 200\cf4 \strokec4 ,\cb1 \
\cb3             \cf7 \strokec7 'body'\cf4 \strokec4 : json.dumps(\cf9 \strokec9 f\cf7 \strokec7 'Successfully processed \cf9 \strokec9 \{\cf4 \strokec4 object_key\cf9 \strokec9 \}\cf7 \strokec7  and stored labels.'\cf4 \strokec4 )\cb1 \
\cb3         \}\cb1 \
\
\cb3     \cf2 \strokec2 except\cf4 \strokec4  \cf12 \strokec12 Exception\cf4 \strokec4  \cf2 \strokec2 as\cf4 \strokec4  e:\cb1 \
\cb3         \cf8 \strokec8 print\cf4 \strokec4 (\cf9 \strokec9 f\cf7 \strokec7 "Error during processing: \cf9 \strokec9 \{\cf12 \strokec12 str\cf4 \strokec4 (e)\cf9 \strokec9 \}\cf7 \strokec7 "\cf4 \strokec4 )\cb1 \
\cb3         \cf5 \strokec5 # Potentially more specific error handling here\cf4 \cb1 \strokec4 \
\cb3         \cf5 \strokec5 # (e.g., catch rekognition_client.exceptions.InvalidS3ObjectException)\cf4 \cb1 \strokec4 \
\cb3         \cf2 \strokec2 return\cf4 \strokec4  \{\cb1 \
\cb3             \cf7 \strokec7 'statusCode'\cf4 \strokec4 : \cf11 \strokec11 500\cf4 \strokec4 ,\cb1 \
\cb3             \cf7 \strokec7 'body'\cf4 \strokec4 : json.dumps(\cf9 \strokec9 f\cf7 \strokec7 'Error processing \cf9 \strokec9 \{\cf4 \strokec4 object_key\cf9 \strokec9 \}\cf7 \strokec7 : \cf9 \strokec9 \{\cf12 \strokec12 str\cf4 \strokec4 (e)\cf9 \strokec9 \}\cf7 \strokec7 '\cf4 \strokec4 )\cb1 \
\cb3         \}\cb1 \
}