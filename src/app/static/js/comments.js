var dispSuccess = function (response) {
	console.log(response);
}

var dispError = function (jqXHR, textStatus, errorThrown) {
	console.log(textStatus);
};

var addQuestionComment = function () {
	var div = $("#add-question-comment");
	var body = $("#comment-body").val();
	var user_id = div.data("user-id");
	var question_id = div.data("question-id");
	console.log(user_id);
	console.log(question_id);
	var url = $SCRIPT_ROOT + '/addQuestionComment';
	console.log(url);
	$.ajax({
		type: "POST",
		url: url,
		data: {user_id: user_id, question_id: question_id, body: body},
		error: dispError,
		success: function (response) {
			var comment = "<li>" + "<div class=\"comment-main-level\" >" 
					+ "<div class=\"comment-avatar\"><img src=\"" + response['avatar'] + "\" alt=\"\"></div>" 
					+ "<div class=\"comment-box\">" 
					+ "<div class=\"comment-head\">" 
					+ "<h6 class=\"comment-name by-author\">"
					+ "<span class=\"comment-author\">"
						+ response['username']
					+ "</span>"
					+ "</h6>"
					+ "<a id=\"downvote-" + response['comment_id'] + "\" onclick=\"downvote(this)\">"
						+ "<i class=\"fa fa-thumbs-down\"> 0 </i>"
					+ "</a>"
					+ "<a id=\"upvote-" + response['comment_id'] + "\" onclick=\"upvote(this)\">"
						+ "<i class=\"fa fa-thumbs-up\"> 0</i>"
					+ "</a>"
					+ "</div>"
					+ "<div class=\"comment-content\" style=\"text-align: justify;\">"
					+ response['body']
					+ "</div>"
					+ "</div>"
					+ "</div>" + "</li>";
			//var ul = $(button).closest('#comments-list');
			$("#add-question-comment").closest('li').before(comment);
			$("#add-question-comment textarea").val("");
			//window.location = response;
			//dispSuccess(response);
		},
	});
}

var addAnswerComment = function (button) {
	var div = $(button).closest('.comment-main-level');
	var user_id = div.data("user-id");
	var answer_id = div.data("answer-id");
	var body_id = "#comment-body-" + answer_id.toString();
	var body = $(body_id).val();
	var url = $SCRIPT_ROOT + '/addAnswerComment';
	$.ajax({
		type: "POST",
		url: url,
		data: {user_id: user_id, answer_id: answer_id, body: body},
		error: dispError,
		success: function (response) {
			var comment = "<li>" + "<div class=\"comment-main-level\" >" 
					+ "<div class=\"comment-avatar\"><img src=\"" + response['avatar'] + "\" alt=\"\"></div>" 
					+ "<div class=\"comment-box\">" 
					+ "<div class=\"comment-head\">" 
					+ "<h6 class=\"comment-name by-author\">"
					+ "<span class=\"comment-author\">"
						+ response['username']
					+ "</span>"
					+ "</h6>"
					+ "<a id=\"downvote-" + response['comment_id'] + "\" onclick=\"downvote(this)\">"
						+ "<i class=\"fa fa-thumbs-down\"> 0 </i>"
					+ "</a>"
					+ "<a id=\"upvote-" + response['comment_id'] + "\" onclick=\"upvote(this)\">"
						+ "<i class=\"fa fa-thumbs-up\"> 0</i>"
					+ "</a>"
					+ "</div>"
					+ "<div class=\"comment-content\" style=\"text-align: justify;\">"
					+ response['body']
					+ "</div>"
					+ "</div>"
					+ "</div>" + "</li>";
			var ul = $(button).closest('#comments-list');
			$(body_id).closest('li').before(comment);
			$(body_id).val("");
		},
	});
}

var upvote = function (button) {
	var id = button.id;
	var comment_id = id.slice(id.search("upvote")+7);
	console.log(comment_id);
	url = $SCRIPT_ROOT + "/commentUpvote" + "/" + comment_id;
	$.ajax({
		type: "GET",
		url: url,
		error: dispError,
		success: function (response) {
			$("#"+id).html("<i class=\"fa fa-thumbs-up\">" + response["upvotes"] + "</i>");
		},
	});
}

var downvote = function (button) {
	var id = button.id;
	var comment_id = id.slice(id.search("downvote")+9);
	console.log(comment_id);
	url = $SCRIPT_ROOT + "/commentDownvote" + "/" + comment_id;
	$.ajax({
		type: "GET",
		url: url,
		error: dispError,
		success: function (response) {
			$("#"+id).html("<i class=\"fa fa-thumbs-down\">" + response["downvotes"] + "</i>");
		},
	});
}

var questionDownvote = function (button) {
	var id = button.id;
	var question_id = id.slice(id.search("downvote")+9);
	console.log(question_id);
	url = $SCRIPT_ROOT + "/questionDownvote" + "/" + question_id;
	$.ajax({
		type: "GET",
		url: url,
		error: dispError,
		success: function (response) {
			$("#"+id).html("Downvotes: <span style=\"font-weight: bold;\">" + response["downvotes"] + "</span>");
		},
	});
}

var questionUpvote = function (button) {
	var id = button.id;
	console.log(button);
	var question_id = id.slice(id.search("upvote")+7);
	console.log(question_id);
	url = $SCRIPT_ROOT + "/questionUpvote" + "/" + question_id;
	console.log(url);
	$.ajax({
		type: "GET",
		url: url,
		error: dispError,
		success: function (response) {
			console.log(response["upvotes"]);
			$("#"+id).html("Upvotes: <span style=\"font-weight: bold;\">" + response["upvotes"] + "</span>");
		},
	});
}

var answerUpvote = function (button) {

	var id = button.id;
	var answer_id = id.slice(id.search("upvote")+7);
	console.log(answer_id);
	url = $SCRIPT_ROOT + "/answerUpvote" + "/" + answer_id;
	$.ajax({
		type: "GET",
		url: url,
		error: dispError,
		success: function (response) {
			$("#"+id).html("Upvotes: <span style=\"font-weight: bold;\">" + response["upvotes"] + "</span>");
		},
	});
}

var answerDownvote = function (button) {
	var id = button.id;
	var answer_id = id.slice(id.search("downvote")+9);
	console.log(answer_id);
	url = $SCRIPT_ROOT + "/answerDownvote" + "/" + answer_id;
	$.ajax({
		type: "GET",
		url: url,
		error: dispError,
		success: function (response) {
			$("#"+id).html("Downvotes: <span style=\"font-weight: bold;\">" + response["downvotes"] + "</span>");
		},
	});
}




























